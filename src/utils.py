"""
Utility functions
"""

def get_paragraphs(story: str, split_str: str = "\n\n") -> list[str]:
    """Returns list of the paragraphs by spliting on the desired split_str"""
    return story.split(split_str)
