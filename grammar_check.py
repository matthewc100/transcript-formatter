import language_tool_python
import re

def fix_extra_spaces(text):
    text = text.replace('\u00A0', ' ')  # non-breaking space
    text = text.replace('\t', ' ')      # tabs
    text = re.sub(r'\s{2,}', ' ', text)  # multiple spaces
    text = re.sub(r' +\n', '\n', text)  # trailing spaces before newline
    return text

AUTO_FIX_RULES = {
    "TOO_MANY_SPACES": fix_extra_spaces,
}

IGNORED_RULE_IDS = {
    "UPPERCASE_SENTENCE_START",
    "INFORMAL_ENGLISH",
    "EN_QUOTES",
    "REDUNDANT_PHRASE"
}

def get_grammar_tool():
    return language_tool_python.LanguageTool('en-US')

def check_paragraph(paragraph, tool):
    matches = tool.check(paragraph)
    results = []
    for match in matches:
        if match.ruleId in IGNORED_RULE_IDS:
            continue
        results.append({
            "ruleId": match.ruleId,
            "message": match.message,
            "context": match.context,
            "suggestions": match.replacements,
            "offset": match.offset,
            "length": match.errorLength
        })
    return results

def apply_auto_fixes(paragraph, tool):
    fixed_text = paragraph
    for rule_id, fix_fn in AUTO_FIX_RULES.items():
        fixed_text = fix_fn(fixed_text)
    return fixed_text
