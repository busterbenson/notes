#!/usr/bin/env python3
"""
Substack to Jekyll Post Converter
Converts Substack posts to Jekyll-formatted markdown files for busterbenson.com
"""

import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, urljoin
import yaml
from pathlib import Path

class SubstackConverter:
    def __init__(self, base_dir="/Users/buster/projects/notes"):
        self.base_dir = Path(base_dir)
        self.assets_dir = self.base_dir / "assets" / "images" / "pieces"
        self.posts_dir = self.base_dir / "_posts"
        
        # Ensure directories exist
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.posts_dir.mkdir(parents=True, exist_ok=True)
    
    def normalize_text(self, text):
        """Strip line breaks and normalize whitespace in text"""
        if not text:
            return text
        return re.sub(r'\s+', ' ', text.strip())
        
    def fetch_post(self, url):
        """Fetch and parse the Substack post"""
        print(f"Fetching post from {url}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            sys.exit(1)
    
    def extract_post_data(self, soup, original_url):
        """Extract the main post content and metadata"""
        post_data = {
            'title': '',
            'subtitle': '',
            'date': '',
            'content': '',
            'images': [],
            'youtube_videos': [],
            'original_url': original_url
        }
        
        # Extract title
        title_elem = soup.find('h1', class_='post-title') or soup.find('h1')
        if title_elem:
            post_data['title'] = self.normalize_text(title_elem.get_text())
        
        # Extract subtitle - look for common Substack subtitle patterns
        subtitle_elem = (
            soup.find('h2', class_='subtitle') or
            soup.find('p', class_='subtitle') or
            soup.find(class_=re.compile(r'subtitle|description|deck')) or
            soup.find('h2') or  # Sometimes the first h2 is the subtitle
            soup.select_one('h1 + p')  # Paragraph immediately after title
        )
        
        if subtitle_elem and subtitle_elem != title_elem:
            subtitle_text = self.normalize_text(subtitle_elem.get_text())
            # Only use as subtitle if it's not too long and not the main content
            if subtitle_text and len(subtitle_text) < 200 and subtitle_text != post_data['title']:
                post_data['subtitle'] = subtitle_text
        
        # Extract date - look for various date patterns in Substack
        date_elem = (soup.find('time') or 
                    soup.find(class_=re.compile('date')) or
                    soup.find(attrs={'datetime': True}) or
                    soup.find(string=re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b')))
        
        if date_elem:
            date_str = date_elem.get('datetime') if hasattr(date_elem, 'get') else str(date_elem)
            if not date_str and hasattr(date_elem, 'get_text'):
                date_str = date_elem.get_text()
            
            try:
                # Try parsing various date formats
                formats = [
                    '%Y-%m-%d', 
                    '%Y-%m-%dT%H:%M:%S', 
                    '%Y-%m-%dT%H:%M:%S.%f',
                    '%B %d, %Y',
                    '%m/%d/%Y',
                    '%d %B %Y'
                ]
                
                for fmt in formats:
                    try:
                        clean_date = date_str.split('T')[0] if 'T' in date_str else date_str.strip()
                        post_data['date'] = datetime.strptime(clean_date, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # Try to extract date from URL as fallback
                    url_match = re.search(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', original_url)
                    if url_match:
                        year, month, day = url_match.groups()
                        post_data['date'] = datetime(int(year), int(month), int(day))
                    else:
                        post_data['date'] = datetime.now()
            except:
                post_data['date'] = datetime.now()
        else:
            # Try to extract date from URL as fallback
            url_match = re.search(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', original_url)
            if url_match:
                year, month, day = url_match.groups()
                post_data['date'] = datetime(int(year), int(month), int(day))
            else:
                print("Warning: Could not find publish date, using current date")
                post_data['date'] = datetime.now()
        
        # Extract main content - look for the post body with Substack-specific patterns
        content_container = (
            soup.find('div', class_='available-content') or
            soup.find('div', class_='post-content') or
            soup.find('div', class_='body markup') or
            soup.find('div', class_='markup') or
            soup.find('article') or
            soup.select_one('[data-testid="post-content"]')
        )
        
        if not content_container:
            # Fallback: look for common Substack content patterns
            potential_containers = soup.find_all(['div', 'article'])
            content_containers_with_text = [c for c in potential_containers if len(c.get_text().strip()) > 100]
            if content_containers_with_text:
                content_container = max(content_containers_with_text, key=lambda x: len(x.get_text()))
        
        if content_container:
            # Extract YouTube videos first
            post_data['youtube_videos'] = self.extract_youtube_embeds(content_container)
            
            # Clean up the content
            post_data['content'] = self.clean_content(content_container, original_url)
            post_data['images'] = self.extract_images(content_container, original_url)
        
        return post_data
    
    def clean_content(self, content_elem, base_url):
        """Clean and convert HTML content to markdown-friendly format"""
        # Remove unwanted elements
        for elem in content_elem.find_all(['script', 'style', 'nav', 'header', 'footer']):
            elem.decompose()
        
        # Remove subscription boxes and other Substack-specific elements
        for elem in content_elem.find_all(class_=re.compile(r'subscribe|paywall|signup|social')):
            elem.decompose()
        
        # Simplified approach - just extract text from common elements
        content_parts = []
        
        # Get all paragraphs, headers, lists
        for elem in content_elem.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'blockquote']):
            if elem.name.startswith('h'):
                level = int(elem.name[1])
                text = elem.get_text().strip()
                if text:
                    content_parts.append(f"{'#' * level} {text}")
            elif elem.name == 'p':
                text = elem.get_text().strip()
                if text and len(text) > 10:  # Skip very short paragraphs
                    content_parts.append(text)
            elif elem.name == 'blockquote':
                text = elem.get_text().strip()
                if text:
                    content_parts.append(f"> {text}")
            elif elem.name in ['ul', 'ol']:
                for li in elem.find_all('li'):
                    li_text = li.get_text().strip()
                    if li_text:
                        content_parts.append(f"- {li_text}")
        
        # Also check for YouTube iframes in the content
        for iframe in content_elem.find_all('iframe'):
            src = iframe.get('src', '')
            if 'youtube.com/embed' in src:
                video_id = src.split('/embed/')[1].split('?')[0]
                if video_id:
                    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                    content_parts.append(f'{{% youtube "{youtube_url}" %}}')
        
        content = '\n\n'.join(content_parts)
        
        # Clean up extra whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content.strip()
    
    def extract_images(self, content_elem, base_url):
        """Extract all images from the content"""
        images = []
        for img in content_elem.find_all('img'):
            src = img.get('src')
            if src:
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = urljoin(base_url, src)
                
                images.append({
                    'url': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        return images
    
    def extract_youtube_embeds(self, content_elem):
        """Extract YouTube video embeds from the content"""
        youtube_videos = []
        
        # Look for YouTube iframes
        for iframe in content_elem.find_all('iframe'):
            src = iframe.get('src', '')
            if 'youtube.com/embed' in src or 'youtu.be' in src:
                # Extract video ID from various YouTube URL formats
                video_id = None
                if '/embed/' in src:
                    video_id = src.split('/embed/')[1].split('?')[0]
                elif 'v=' in src:
                    video_id = src.split('v=')[1].split('&')[0]
                
                if video_id:
                    youtube_videos.append({
                        'video_id': video_id,
                        'iframe_element': iframe
                    })
        
        return youtube_videos
    
    def download_images(self, images, post_slug, post_date):
        """Download images and return local paths"""
        local_images = []
        
        for i, img in enumerate(images):
            try:
                response = requests.get(img['url'])
                response.raise_for_status()
                
                # Determine file extension
                parsed_url = urlparse(img['url'])
                ext = os.path.splitext(parsed_url.path)[1] or '.jpg'
                
                # Create filename with date prefix for better organization
                date_prefix = post_date.strftime('%Y-%m-%d')
                filename = f"{date_prefix}-{post_slug}-{i+1:02d}{ext}"
                filepath = self.assets_dir / filename
                
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Store full path for Jekyll responsive images
                full_path = f"assets/images/pieces/{filename}"
                local_images.append({
                    'filename': full_path,
                    'alt': img['alt'],
                    'title': img['title']
                })
                
                print(f"Downloaded image: pieces/{filename}")
                
            except Exception as e:
                print(f"Warning: Could not download image {img['url']}: {e}")
                continue
        
        return local_images
    
    def create_front_matter(self, post_data, local_images):
        """Generate Jekyll front matter"""
        # Create slug from title
        slug = re.sub(r'[^\w\s-]', '', post_data['title']).strip()
        slug = re.sub(r'[-\s]+', '-', slug).lower()
        
        front_matter = {
            'title': self.normalize_text(post_data['title']),
            'link': post_data['original_url'],
            'author': 'me',
            'redirect': False
        }
        
        # Only add featured image if there's a good hero image
        # For now, don't auto-add featured images - let them be inline
        front_matter['image'] = ""
        
        # Use extracted subtitle as one_liner if available
        if post_data['subtitle']:
            front_matter['one_liner'] = self.normalize_text(post_data['subtitle'])
            print(f"Using extracted subtitle as one_liner: {post_data['subtitle']}")
        
        # Interactive prompts for additional metadata (if terminal available)
        print(f"\nPost title: {post_data['title']}")
        print(f"Post date: {post_data['date'].strftime('%Y-%m-%d')}")
        
        try:
            # Only ask for one_liner if we didn't extract a subtitle
            if not post_data['subtitle']:
                one_liner = input("One-liner description (optional): ").strip()
                if one_liner:
                    front_matter['one_liner'] = self.normalize_text(one_liner)
            else:
                # Allow overriding the extracted subtitle
                override_one_liner = input(f"Override one-liner (current: '{post_data['subtitle']}'): ").strip()
                if override_one_liner:
                    front_matter['one_liner'] = self.normalize_text(override_one_liner)
            
            piles_input = input("Piles (comma-separated, optional): ").strip()
            if piles_input:
                piles = [self.normalize_text(pile) for pile in piles_input.split(',') if pile.strip()]
                front_matter['piles'] = piles
        except (EOFError, KeyboardInterrupt):
            print("\nNo interactive input available - using extracted metadata")
        
        return front_matter, slug
    
    def generate_markdown_file(self, post_data, front_matter, slug, local_images):
        """Generate the complete markdown file"""
        date = post_data['date']
        year_dir = self.posts_dir / str(date.year)
        year_dir.mkdir(exist_ok=True)
        
        # Create filename
        filename = f"{date.strftime('%Y-%m-%d')}-{slug}.md"
        filepath = year_dir / filename
        
        # Generate front matter YAML 
        yaml_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True, width=1000)
        
        # Create content with responsive images placed inline
        content = post_data['content']
        
        # Place images contextually within the content
        if local_images:
            content_lines = content.split('\n\n')
            
            # Try to place images at strategic locations
            for i, img in enumerate(local_images):
                alt_attr = f" alt:'{img['alt']}'" if img['alt'] else ""
                img_syntax = f"{{% responsive_image path:'{img['filename']}'{alt_attr} %}}"
                
                if i == 0:
                    # First image: place after the first few paragraphs or before first heading
                    insertion_point = min(3, len(content_lines) // 2)
                    for j in range(insertion_point, len(content_lines)):
                        if content_lines[j].startswith('#'):
                            insertion_point = j
                            break
                    content_lines.insert(insertion_point, img_syntax)
                else:
                    # Additional images: place near the end or before conclusion
                    insertion_point = max(len(content_lines) - 3, len(content_lines) // 2)
                    content_lines.insert(insertion_point, img_syntax)
            
            content = '\n\n'.join(content_lines)
        
        # Combine everything
        full_content = f"---\n{yaml_front_matter}---\n\n{content}"
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"\nCreated post: {filepath}")
        return filepath
    
    def convert(self, url):
        """Main conversion function"""
        # Fetch and parse the post
        soup = self.fetch_post(url)
        
        # Extract post data
        post_data = self.extract_post_data(soup, url)
        
        if not post_data['title']:
            print("Error: Could not extract post title")
            sys.exit(1)
        
        print(f"Found post: {post_data['title']}")
        if post_data['subtitle']:
            print(f"Subtitle: {post_data['subtitle']}")
        print(f"Date: {post_data['date'].strftime('%Y-%m-%d')}")
        print(f"Found {len(post_data['images'])} images")
        print(f"Found {len(post_data['youtube_videos'])} YouTube videos")
        print(f"Content length: {len(post_data['content'])} characters")
        
        # Create slug for filenames
        slug = re.sub(r'[^\w\s-]', '', post_data['title']).strip()
        slug = re.sub(r'[-\s]+', '-', slug).lower()
        
        # Download images
        local_images = self.download_images(post_data['images'], slug, post_data['date'])
        
        # Create front matter
        front_matter, final_slug = self.create_front_matter(post_data, local_images)
        
        # Generate markdown file
        filepath = self.generate_markdown_file(post_data, front_matter, final_slug, local_images)
        
        print(f"\n✅ Conversion complete!")
        print(f"Post saved to: {filepath}")
        
        return filepath

def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_substack.py <substack_url>")
        print("Example: python convert_substack.py https://buster.substack.com/p/some-post")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Validate URL
    if 'substack.com' not in url:
        print("Error: This script is designed for Substack URLs")
        sys.exit(1)
    
    converter = SubstackConverter()
    converter.convert(url)

if __name__ == "__main__":
    main()