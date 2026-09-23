#we need a function that can look at any raw value and figure out for itself: "is this an IP? A domain? A URL? A hash? An email?" — using pattern recognition, not relying on the file to tell us.
import re # used for pattern matching also called regex(regular expression) 
import ipaddress # tool for validating IP addresses properly we could try this with regex but there are many ip addresses which are not valid so this module looks for those addresses
#recognising URL pattern-
#almost every URL starts with http:// or https://
url_pattern=re.compile(r"^https?://",re.IGNORECASE)
def is_url(value):
    return bool(url_pattern.match(value))
#Quick explanation, piece by piece:
#re.compile(...) → this "prepares" a pattern once, so Python doesn't have to re-interpret it every single time we check a value. We store it in a variable so we can reuse it.
#r"^https?://" → this is the actual pattern, written in regex language:
#The r before the quotes means "raw string" — tells Python not to treat backslashes specially (regex uses a lot of them).
#^ → means "must start at the very beginning of the text."
#https? → the ? means "the s is optional" — so this matches both http and https.
#:// → just the literal characters ://.
#re.IGNORECASE → makes it match HTTP:// or Http:// too, not just lowercase.
#def is_url(value): → our function, takes one value and checks it.
#URL_PATTERN.match(value) → checks if value matches our pattern at the start. This returns either a "match object" (if it matches) or none 

# recognising email pattern-
# emails always look like: something@something.something

def is_email(value):
    return bool(email_pattern.match(value))
email_pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
# recognising hash pattern-
# hashes are hex strings (only a-f, A-F, 0-9) of a fixed length depending on algorithm
md5_pattern=re.compile(r"^[a-fA-f0-9]{32}$")
sha1_pattern=re.compile(r"^[a-fA-F0-9]{40}$")
sha256_pattern=re.compile(r"^[a-fA-F0-9]{64}$")
def is_hash(value):
    return bool(
        md5_pattern.match(value)
        or sha1_pattern.match(value)
        or sha256_pattern.match(value)
    )

#Why this one's checked later: domains have the loosest, most generic pattern — just word.word. 
# If we checked this too early, it could accidentally swallow up things that are actually URLs or emails. 
# That's why it comes near the end, as more of a fallback.

# recognising domain pattern-
# domains look like word.word (e.g. example.com) - checked last since it's the most generic shape
domain_pattern = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
def is_domain(value):
    return bool(domain_pattern.match(value))

## recognising ip pattern-
# using Python's built-in ipaddress module instead of regex, since it correctly
# rejects invalid-looking IPs (e.g. 999.999.999.999) that a regex might wrongly accept
def is_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False

# main function - checks each pattern in order from most specific to most generic,
# so nothing gets misclassified (e.g. a URL containing an IP is still labeled as a URL)
def detect_type(value):
    value=value.strip()
    if is_url(value):
        return "url"
    if is_email(value):
        return "email"
    if is_hash(value):
        return "hash"
    if is_ip(value):
        return "ip"
    if  is_domain(value):
        return "domain"
    return "unknown"

if __name__=="__main__":
    test_values = [
        "185.220.101.4",
        "badactor-phish.net",
        "http://free-gift-cards-now.biz/claim",
        "5d41402abc4b2a76b9719d911017c592",
        "attacker@malicious-update-portal.com",
        "not a real indicator at all",
    ]
    for i in test_values:
        print(f"{i!r:55} -> {detect_type(i)}")