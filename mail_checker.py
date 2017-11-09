import re


################################################################################
### Rules
################################################################################

# 1. Mail consists of two parts: name and domain. These parts are separated by
#    the symbol '@'.
RULE_1_SEPARATOR = '@'

# 2. Domain is not shorter than 3 characters and not longer than 256 characters.
#    Domain consists of subdomains separated by '.'
#    Characters allowed in a subdomain: 'a-z0-9_-'
RULE_2_REGEXP = re.compile(r'^[.a-z0-9_-]{3,256}$')
RULE_2_SEPARATOR = '.'

# 3. Each subdomain cannot start or end with the '-' symbol.
RULE_3_SYMBOL = '-'

# 4. Name is not longer than 128 characters.
#    Characters allowed in it: 'a-z0-9"._-'
#    Extra characters allowed inside double quotes: '!,:'
RULE_4_REGEXP = re.compile(r'^[a-z0-9"._!,:-]{1,128}$')

# 5. Name cannot have '..' in it.
RULE_5_SYMBOLS = '..'

# 6. Double quotes inside name must be paired.
RULE_6_SYMBOL = '"'
RULE_6_PAIR = '".*?"'

# 7. Inside name the characters '!,:' can occur only between double quotes.
RULE_7_REGEXP = re.compile(r'[!,:]')


################################################################################
### Errors
################################################################################

(ERR_RULE_1, ERR_RULE_2, ERR_RULE_3, ERR_RULE_4,
 ERR_RULE_5, ERR_RULE_6, ERR_RULE_7) = range(7)


################################################################################
### Checker
################################################################################

def check(mail):
    """Return None if mail obeys the rules. Return error code otherwise."""

    # Rule 1
    try:
        name, domain = mail.split(RULE_1_SEPARATOR)
    except ValueError:
        return ERR_RULE_1

    # Rules 2, 3
    if not RULE_2_REGEXP.match(domain):
        return ERR_RULE_2
    subdomains = domain.split(RULE_2_SEPARATOR)
    for subdomain in subdomains:
        if not subdomain:
            return ERR_RULE_2
        if (subdomain.startswith(RULE_3_SYMBOL) or
                subdomain.endswith(RULE_3_SYMBOL)):
            return ERR_RULE_3

    # Rule 4
    if not RULE_4_REGEXP.match(name):
        return ERR_RULE_4

    # Rule 5
    if RULE_5_SYMBOLS in name:
        return ERR_RULE_5

    # Rules 6, 7
    name_without_pairs = re.sub(RULE_6_PAIR, '', name)
    if RULE_6_SYMBOL in name_without_pairs:
        return ERR_RULE_6
    if RULE_7_REGEXP.search(name_without_pairs):
        return ERR_RULE_7

    return None
