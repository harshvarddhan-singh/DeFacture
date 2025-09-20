"""
Fact-Check Agent for DeFacture

This module implements a fact-checking pipeline for verifying extracted claims.
Currently uses mock verification logic that can be extended with LangChain and real sources.
"""

import re
import random
import logging
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fact_check_claims(claims: List[Dict]) -> List[Dict]:
    """
    Fact-check a list of extracted claims using mock verification pipeline
    
    Parameters:
    -----------
    claims : List[Dict]
        List of claims from extraction agent, each with 'claim' and 'confidence'
        
    Returns:
    --------
    List[Dict]
        List of fact-checked claims with verdict and justification
        Format: [{"claim": str, "confidence": float, "verdict": str, "justification": str}, ...]
    """
    if not claims:
        return []
        
    logger.info(f"Starting fact-check for {len(claims)} claims")
    
    fact_checked_claims = []
    
    for claim_data in claims:
        claim_text = claim_data.get("claim", "")
        confidence = claim_data.get("confidence", 0.5)
        
        # Mock fact-checking logic
        verdict, justification = _mock_fact_check_claim(claim_text, confidence)
        
        fact_checked_claims.append({
            "claim": claim_text,
            "confidence": confidence,
            "verdict": verdict,
            "justification": justification
        })
    
    logger.info(f"Completed fact-check for {len(fact_checked_claims)} claims")
    return fact_checked_claims

def _mock_fact_check_claim(claim: str, confidence: float) -> tuple:
    """
    Mock fact-checking for a single claim
    In production, this would be replaced with real verification against sources
    
    Parameters:
    -----------
    claim : str
        The claim text to fact-check
    confidence : float
        Original confidence score from extraction
        
    Returns:
    --------
    tuple
        (verdict, justification) where verdict is "Accurate", "Partially Accurate", or "False"
    """
    claim_lower = claim.lower()
    
    # Mock logic based on keyword patterns and confidence
    
    # High confidence claims with research/data indicators tend to be accurate
    if confidence >= 0.8 and any(word in claim_lower for word in 
        ['research', 'study', 'data', 'published', 'according to', 'survey']):
        return _generate_accurate_verdict(claim)
    
    # Medical/scientific claims
    if any(word in claim_lower for word in 
        ['clinical trial', 'patients', 'treatment', 'medical', 'university', 'hospital']):
        return _generate_medical_verdict(claim)
    
    # Economic/financial claims
    if any(word in claim_lower for word in 
        ['billion', 'million', 'percent', '%', 'economy', 'financial', 'market']):
        return _generate_economic_verdict(claim)
    
    # Technology/company claims
    if any(word in claim_lower for word in 
        ['company', 'tech', 'ai', 'artificial intelligence', 'summit', 'innovation']):
        return _generate_tech_verdict(claim)
    
    # Government/policy claims
    if any(word in claim_lower for word in 
        ['government', 'policy', 'regulation', 'minister', 'president', 'official']):
        return _generate_government_verdict(claim)
    
    # Climate/environmental claims
    if any(word in claim_lower for word in 
        ['climate', 'temperature', 'warming', 'emissions', 'environmental']):
        return _generate_climate_verdict(claim)
    
    # Default: assign verdict based on confidence with some randomness
    if confidence >= 0.7:
        verdicts = ["Accurate", "Partially Accurate"]
        weights = [0.7, 0.3]
    elif confidence >= 0.5:
        verdicts = ["Accurate", "Partially Accurate", "False"]
        weights = [0.4, 0.4, 0.2]
    else:
        verdicts = ["Partially Accurate", "False"]
        weights = [0.6, 0.4]
    
    verdict = random.choices(verdicts, weights=weights)[0]
    justification = _generate_default_justification(verdict, confidence)
    
    return verdict, justification

def _generate_accurate_verdict(claim: str) -> tuple:
    """Generate accurate verdict with appropriate justification"""
    justifications = [
        "Matches official data and verified sources.",
        "Confirmed by peer-reviewed research publications.",
        "Consistent with authoritative government statistics.",
        "Verified against multiple reliable news sources.",
        "Supported by academic research and official reports."
    ]
    return "Accurate", random.choice(justifications)

def _generate_medical_verdict(claim: str) -> tuple:
    """Generate medical claim verdict"""
    verdicts_justifications = [
        ("Accurate", "Verified against clinical trial databases and medical journals."),
        ("Accurate", "Consistent with peer-reviewed medical research findings."),
        ("Partially Accurate", "Core facts correct but some details may need verification."),
        ("Partially Accurate", "Treatment data accurate but timeline claims need confirmation.")
    ]
    return random.choice(verdicts_justifications)

def _generate_economic_verdict(claim: str) -> tuple:
    """Generate economic claim verdict"""
    verdicts_justifications = [
        ("Accurate", "Confirmed by official economic data and financial reports."),
        ("Accurate", "Matches government economic statistics and market data."),
        ("Partially Accurate", "Financial figures correct but context may be incomplete."),
        ("False", "Contradicts official economic data from authoritative sources.")
    ]
    return random.choice(verdicts_justifications)

def _generate_tech_verdict(claim: str) -> tuple:
    """Generate technology claim verdict"""
    verdicts_justifications = [
        ("Accurate", "Confirmed by official company announcements and tech news."),
        ("Accurate", "Verified through industry reports and summit documentation."),
        ("Partially Accurate", "Company data accurate but innovation claims are subjective."),
        ("Partially Accurate", "Attendance figures correct but impact assessments vary.")
    ]
    return random.choice(verdicts_justifications)

def _generate_government_verdict(claim: str) -> tuple:
    """Generate government/policy claim verdict"""
    verdicts_justifications = [
        ("Accurate", "Verified through official government sources and records."),
        ("Accurate", "Consistent with public policy documents and announcements."),
        ("Partially Accurate", "Policy details correct but implementation timeline unclear."),
        ("False", "Contradicts official government statements and documentation.")
    ]
    return random.choice(verdicts_justifications)

def _generate_climate_verdict(claim: str) -> tuple:
    """Generate climate/environmental claim verdict"""
    verdicts_justifications = [
        ("Accurate", "Supported by climate science data and IPCC reports."),
        ("Accurate", "Consistent with peer-reviewed environmental research."),
        ("Partially Accurate", "Temperature data correct but projections have uncertainty."),
        ("Partially Accurate", "Environmental trends accurate but timeline estimates vary.")
    ]
    return random.choice(verdicts_justifications)

def _generate_default_justification(verdict: str, confidence: float) -> str:
    """Generate default justification based on verdict and confidence"""
    if verdict == "Accurate":
        return f"Claim appears credible based on available information (confidence: {int(confidence*100)}%)."
    elif verdict == "Partially Accurate":
        return f"Some aspects verified but additional confirmation needed (confidence: {int(confidence*100)}%)."
    else:  # False
        return f"Claim contradicts available evidence and reliable sources (confidence: {int(confidence*100)}%)."

def get_fact_check_statistics(fact_checked_claims: List[Dict]) -> Dict:
    """
    Generate statistics about fact-checked claims
    
    Parameters:
    -----------
    fact_checked_claims : List[Dict]
        List of fact-checked claims with verdicts
        
    Returns:
    --------
    Dict
        Statistics about the fact-check results
    """
    if not fact_checked_claims:
        return {
            "total_claims": 0,
            "accurate_count": 0,
            "partially_accurate_count": 0,
            "false_count": 0,
            "accuracy_rate": 0.0
        }
    
    verdicts = [claim["verdict"] for claim in fact_checked_claims]
    
    accurate_count = verdicts.count("Accurate")
    partially_accurate_count = verdicts.count("Partially Accurate")
    false_count = verdicts.count("False")
    
    # Calculate accuracy rate (accurate + partially accurate)
    accuracy_rate = (accurate_count + partially_accurate_count) / len(verdicts) if verdicts else 0
    
    return {
        "total_claims": len(verdicts),
        "accurate_count": accurate_count,
        "partially_accurate_count": partially_accurate_count,
        "false_count": false_count,
        "accuracy_rate": round(accuracy_rate, 2)
    }