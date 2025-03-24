# Cosmological Worldview Questionnaire: Project Overview

## Project Structure and Goals

The Cosmological Worldview Questionnaire is designed to help people identify their fundamental beliefs about the nature of reality. Through a carefully structured decision tree of questions, individuals can navigate to one of 68 distinct cosmological perspectives that best matches their worldview.

### Primary goals of this project are:

1. To create an accessible way for people to identify and understand their implicit cosmological assumptions
2. To map the landscape of possible worldviews across religious, philosophical, scientific, and alternative perspectives
3. To use "recognitional language" that reflects how adherents of each perspective would describe their own views
4. To develop the most efficient question path that minimizes the number of questions needed while maximizing accuracy

### File structure
- The cosmologies.csv file has a list of cosmologies and a matrix of statements that show compatibility of the belief system with that statement. The key for R, NR, and DB are defined:  
  - **"R"** (Required): This belief is essential for this cosmological perspective
  - **"DB"** (Deal-Breaker): This belief is incompatible with this cosmological perspective
  - **"NR"** (Not Required): This belief is neither required nor incompatible

## Key Design Principles

### Recognitional Language

A crucial aspect of this questionnaire is the use of "recognitional language" throughout. Rather than describing worldviews from an outside perspective, we use language that adherents would use to describe their own views. For example:

- Instead of "Flat Earth Conspiracy theorists believe Earth is flat," we use "Unlike those who accept mainstream cosmology without question, Flat Earth proponents recognize that sensory evidence suggests Earth is flat."
- We use terms like "recognize," "understand," and "experience" rather than "believe" or "claim."
- We emphasize how adherents see their perspective as resolving problems or revealing truths that other worldviews miss.

This approach helps users genuinely identify with descriptions that resonate with their thinking, rather than feeling their views are being characterized by outsiders.

### Optimized Decision Tree

The questionnaire uses a decision tree structure optimized for efficient filtering:

1. It begins with high-discrimination questions (like Earth's shape) that create clear branches
2. It uses a hierarchical structure where related cosmologies share branches until their distinguishing characteristics
3. Each question typically has 2-6 options that effectively sort the remaining cosmologies
4. Most paths require only 3-5 questions to reach a specific worldview

This structure was developed by analyzing a comprehensive matrix of 68 cosmologies and 78 belief characteristics, identifying which characteristics have the highest "filtering power" at each decision point.

### Comprehensive Coverage

The questionnaire covers a wide spectrum of worldviews:

- Religious perspectives (Young Earth Creationism, Theistic Evolution, Polytheism, etc.)
- Philosophical traditions (various forms of idealism, materialism, dualism)
- Scientific frameworks (Scientific Materialism, Multiverse Theory, etc.)
- Alternative or non-mainstream perspectives (Flat Earth, Ancient Astronaut Theory, etc.)
- Indigenous and animistic worldviews
- Spiritual but non-religious perspectives (New Age approaches, Spiritual Naturalism, etc.)
- Agnostic and skeptical positions

### Matrix of Belief Characteristics

Underlying the questionnaire is a comprehensive matrix that maps each cosmology against 78 belief characteristics. Each cell contains one of three values (R, DB, or NR, as defined above). This matrix allows for detailed analysis of compatibility between different worldviews and identification of the most discriminating belief characteristics.

## Implementation Approach

The questionnaire has been implemented as a single-path decision tree where each question leads to either more specific questions or a final cosmological perspective. The questions have been carefully worded to:

1. Be accessible to people without specialized philosophical knowledge
2. Accurately represent the distinctions between different worldviews
3. Use language that adherents of each perspective would find accurate and respectful
4. Create clear, unambiguous choices at each decision point

## Utilization Guidelines

When implementing or extending this system:

1. **Maintain recognitional language**: Always present each worldview in terms that its adherents would recognize and accept.

2. **Respect the decision tree structure**: The order and branching of questions has been optimized for efficiency based on statistical analysis of filtering power.

3. **Provide detailed cosmology descriptions**: Once a specific cosmology is identified, provide a rich description that helps the person understand the philosophical tradition they align with.

4. **Avoid judgment**: Present all cosmologies as valid perspectives without suggesting some are more rational or defensible than others.

5. **Highlight key distinctions**: When describing similar cosmologies (e.g., different forms of Deism), emphasize the specific characteristics that distinguish them.

6. **Acknowledge complexity**: Recognize that many people hold hybrid views or might find elements of multiple cosmologies appealing.

This project represents a comprehensive mapping of how humans understand reality, developed through a systematic analysis of belief characteristics and their relationships. It serves as both an educational tool for understanding the landscape of possible worldviews and a practical guide for individuals seeking to clarify their own cosmological perspective.
