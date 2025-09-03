#!/usr/bin/env python3
"""
Test script to verify token count is under Groq limits
"""

def count_tokens(text: str) -> int:
    """Estimate token count for a given text using character count"""
    # Rough estimation: 4 characters per token average
    return len(text) // 4

def test_system_prompt():
    """Test the system prompt size"""
    
    # Mock context data
    question_analysis = {
        'complexity_score': 8,
        'requires_analysis': True
    }
    question_types = ['strategic', 'financial']
    has_loaded_content = False
    context_summary = "\nPrevious topics: strategic, market\n"
    content_context = "\n\n📋 MODE: General Business Intelligence (No specific product data loaded)\n- Draw from extensive business knowledge and industry best practices\n- Provide strategic insights and analytical frameworks\n- Offer actionable business recommendations"
    
    # The reduced system prompt
    system_prompt = f"""You are Wolf AI, an expert business consultant with MBA-level expertise.

🎯 EXPERTISE: Strategic analysis, financial modeling, market intelligence, sales strategy, and operational excellence.

📊 SESSION CONTEXT:
- Question Complexity: {question_analysis['complexity_score']}/20
- Categories: {', '.join(question_types) if question_types else 'General business'}
- Analysis Level: {'Deep' if question_analysis['requires_analysis'] else 'Standard'}
- Data: {'Specific business data available' if has_loaded_content else 'General business knowledge'}
{context_summary}
{content_context}

🧠 FRAMEWORKS: Apply SWOT, Porter's Five Forces, ROI analysis, market segmentation, competitive analysis, and strategic planning as appropriate.

💼 RESPONSE APPROACH:
- Strategic questions: Multi-framework analysis with implementation roadmap
- Financial questions: Detailed calculations with assumptions and scenarios
- Market questions: Competitive analysis with positioning recommendations
- Operational questions: Process optimization with efficiency metrics

📋 STANDARDS:
- Use clear structure with headings and bullet points
- Provide actionable recommendations with next steps
- Include quantitative analysis when possible
- Maintain professional consultant-level quality
- Focus on business value and ROI

🔥 MANDATE: Always provide valuable business insights using proven frameworks and best practices. Never refuse to answer due to lack of specific data - leverage extensive business knowledge instead."""

    # Test with a sample user message
    user_message = "What are the key factors to consider when pricing a new product?"
    
    # Simulate conversation history (4 messages)
    conversation_history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello! How can I help you with your business today?"},
        {"role": "user", "content": "Tell me about market analysis"},
        {"role": "assistant", "content": "Market analysis involves understanding your target market, competitors, and industry trends..."}
    ]
    
    # Calculate total token count
    system_tokens = count_tokens(system_prompt)
    user_tokens = count_tokens(user_message)
    history_tokens = sum(count_tokens(msg["content"]) for msg in conversation_history)
    
    total_tokens = system_tokens + user_tokens + history_tokens
    
    print(f"Token count analysis:")
    print(f"- System prompt: {system_tokens} tokens")
    print(f"- User message: {user_tokens} tokens")
    print(f"- Conversation history: {history_tokens} tokens")
    print(f"- Total input tokens: {total_tokens} tokens")
    print(f"- Groq limit: 6000 tokens per minute")
    print(f"- Status: {'✅ WITHIN LIMITS' if total_tokens < 5000 else '❌ EXCEEDS LIMITS'}")
    
    if total_tokens >= 5000:
        print(f"\n⚠️  WARNING: Token count is too high!")
        print(f"Recommended reduction: {total_tokens - 4500} tokens")

if __name__ == "__main__":
    test_system_prompt()
