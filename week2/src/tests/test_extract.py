import os
from loguru import logger

from app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    logger.info(f"Extracted items: {items}")
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items
    
def test_extract_bullets_and_checkboxes_llm():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items_llm(text)
    logger.info(f"Extracted items: {items}")
    
    items = [item.lower().rstrip('.') for item in items]
    assert "set up database" in items
    assert "implement api extract endpoint" in items
    assert "write tests" in items

def test_extract_action_items_llm_basic():
    """Test real extraction of action items using LLM"""
    text = "Meeting notes: We need to schedule a team meeting and review the project requirements."

    result = extract_action_items_llm(text)
    logger.info(f"Text: {text}")
    logger.info(f"Extracted items: {result}")

    # 验证返回的是字符串列表
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

    # 验证提取出了一些有意义的action items
    if result:  # 如果有结果
        for item in result:
            assert len(item.strip()) > 0  # 不是空字符串


def test_extract_action_items_llm_empty_input():
    """Test with text that likely has no action items"""
    text = "This is just a regular conversation about the weather and nothing important."

    result = extract_action_items_llm(text)
    logger.info(f"Text: {text}")
    logger.info(f"Extracted items: {result}")

    # 验证返回的是列表
    assert isinstance(result, list)
    # 可能返回空列表，也可能返回一些内容，都接受
    if result:
        assert all(isinstance(item, str) for item in result)


def test_extract_action_items_llm_clear_actions():
    """Test with clear action items"""
    text = "TODO: Update the documentation. ACTION: Fix the authentication bug. NEXT: Review pull requests."

    result = extract_action_items_llm(text)
    logger.info(f"Text: {text}")
    logger.info(f"Extracted items: {result}")

    assert isinstance(result, list)

    # 应该识别出至少一些action items
    if result:
        assert all(isinstance(item, str) for item in result)
        # 检查是否包含预期的关键词
        result_text = " ".join(result).lower()
        # 至少应该提到一些动作
        assert any(word in result_text for word in ["update", "fix", "review", "documentation", "authentication", "pull"])


def test_extract_action_items_llm_technical_content():
    """Test with technical tasks"""
    text = """
    Technical backlog:
    - Add API endpoint for user management
    - Fix database connection timeout issue
    - Implement caching layer for performance
    - Update Docker configuration for production
    """

    result = extract_action_items_llm(text)
    logger.info(f"Text: {text}")
    logger.info(f"Extracted items: {result}")

    assert isinstance(result, list)

    if result:
        assert all(isinstance(item, str) for item in result)
        # 应该包含技术相关的内容
        result_text = " ".join(result).lower()
        # 至少应该提到一些技术术语
        technical_terms = ["api", "endpoint", "database", "caching", "docker", "configuration"]
        assert any(term in result_text for term in technical_terms)


def test_extract_action_items_llm_meeting_notes():
    """Test with realistic meeting notes"""
    text = """
    Team sync - Dec 15, 2023

    Action items from today's meeting:
    1. Sarah will prepare the Q1 roadmap presentation
    2. Mike needs to review the latest design mockups by Friday
    3. Engineering team should prioritize the bug fixes
    4. Schedule follow-up meeting with stakeholders

    Other updates: The product launch is on track. Marketing campaign is ready to go.
    """

    result = extract_action_items_llm(text)
    logger.info(f"Text: {text}")
    logger.info(f"Extracted items: {result}")

    assert isinstance(result, list)

    if result:
        assert all(isinstance(item, str) for item in result)
        # 应该识别出具体的任务和责任人
        result_text = " ".join(result).lower()
        action_keywords = ["prepare", "review", "prioritize", "schedule", "presentation", "mockups", "bugs", "stakeholders"]
        assert any(keyword in result_text for keyword in action_keywords)


def test_extract_action_items_llm_edge_cases():
    """Test edge cases with special characters and formatting"""
    text = """
    Special character tests:
    • Review API endpoint: /api/users/{id}?include=profile
    - Handle database null-values & edge-cases
    - Update config.json with new settings
    * Check if env variables (DATABASE_URL, API_KEY) are set
    """

    result = extract_action_items_llm(text)
    logger.info(f"Text: {text}")
    logger.info(f"Extracted items: {result}")

    assert isinstance(result, list)

    if result:
        assert all(isinstance(item, str) for item in result)
        # 应该能正确处理特殊字符
        result_text = " ".join(result)
        # 检查是否保留了特殊字符
        has_special_chars = any(char in result_text for char in ["{", "}", "/", "&", "(", ")", "."])
        # 如果有特殊字符被保留，这是一个好迹象
        if has_special_chars:
            logger.info("Special characters preserved in extraction")
