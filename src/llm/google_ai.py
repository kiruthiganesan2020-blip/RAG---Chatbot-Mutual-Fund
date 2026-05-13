"""
Google AI Studio (Gemini) integration for RAG system
"""

import os
import re
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from datetime import datetime

from src.config import settings, get_logger

logger = get_logger(__name__)


class GoogleAIStudioIntegration:
    """Integration with Google AI Studio (Gemini)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.google_ai_studio_api_key
        self.model_name = "gemini-flash-latest"
        self.model = None
        self._setup_client()
        self.hdfc_reference_context = """
        HDFC fund pages covered by this assistant include HDFC Large Cap Fund, HDFC Mid Cap Fund,
        HDFC Equity Fund, HDFC Focused Fund, and HDFC ELSS Tax Saver Fund. These pages are used for
        factual questions about scheme category, NAV, risk, SIP/lumpsum minimums, expense ratio,
        exit load, fund objective, benchmark, portfolio style, and tax-saver/ELSS concepts. When exact
        live figures are not available in retrieved context, explain the concept and tell the user to
        check the latest scheme document or official fund page for current numbers.
        """
        
        # System prompt for compliance and facts-only mode
        self.system_prompt = """
        You are an HDFC Mutual Fund FAQ Assistant. Your goal is to provide accurate,
        factual, and compliant educational information about mutual funds and the
        HDFC fund pages represented in the provided context.
        
        Guidelines:
        1. Use the provided search results first whenever they contain relevant facts.
        2. If the provided context is incomplete but the question is clearly about
           mutual fund concepts, fund categories, NAV, risk, returns, SIPs, expense
           ratio, exit load, tax saver/ELSS, or the HDFC fund pages in context,
           answer using general mutual-fund knowledge in a careful educational way.
        3. If the question is unrelated to mutual funds or HDFC fund information,
           say that you can only help with mutual-fund related questions.
        4. Do NOT provide financial advice or recommendations (e.g., don't say "you should invest").
        5. Use a professional, helpful tone.
        6. Keep responses concise (maximum 3 sentences unless requested otherwise).
        7. Always include a disclaimer that mutual fund investments are subject to market risks.
        8. If providing exact data like NAV, returns, AUM, Expense Ratio, or Exit Load,
           use the context when available and mention the source/date if present.
           If exact current data is not present, explain the concept and suggest
           checking the latest scheme documents or official fund page for current figures.
        """

    def _setup_client(self):
        """Initialize Gemini client"""
        try:
            if not self.api_key:
                logger.warning("GOOGLE_AI_STUDIO_API_KEY not configured. Falling back to local summarization.")
                return
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Gemini client initialized with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.model = None

    def generate_response(
        self, 
        query: str, 
        search_results: List[Dict[str, Any]], 
        intent: str = "factual"
    ) -> Dict[str, Any]:
        """Generate response based on query and search results"""
        try:
            if not self._is_mutual_fund_related(query):
                return {
                    'response': "I can help with mutual-fund related questions, especially questions about HDFC Mutual Fund schemes, NAV, SIPs, risk, returns, expense ratios, exit loads, and ELSS/tax-saver funds.",
                    'source_documents': [],
                    'confidence': 0.0,
                    'intent': intent,
                    'timestamp': datetime.now().isoformat(),
                    'model_used': "scope_guard"
                }

            # Prepare context from search results
            context = self._build_context(search_results)
            exact_response = self._extract_structured_answer(query, search_results)
            if exact_response:
                return {
                    'response': exact_response,
                    'source_documents': [res.get('id', 'unknown') for res in search_results[:2]],
                    'confidence': self._calculate_confidence(search_results),
                    'intent': intent,
                    'timestamp': datetime.now().isoformat(),
                    'model_used': "context_extractor"
                }
            
            if not context:
                fallback_response = self._generate_common_faq_response(query)
                if fallback_response:
                    return {
                        'response': fallback_response,
                        'source_documents': [],
                        'confidence': 0.5,
                        'intent': intent,
                        'timestamp': datetime.now().isoformat(),
                        'model_used': "local_educational_fallback"
                    }
            
            # Generate response using LLM or local fallback
            if self.model:
                response_text = self._generate_with_gemini(query, context, intent)
            else:
                response_text = self._generate_factual_response(context, query)

            if self._is_unhelpful_response(response_text):
                common_response = self._generate_common_faq_response(query)
                if common_response:
                    response_text = common_response
                elif self.model:
                    response_text = self._generate_with_gemini(
                        query,
                        "The retrieved fund-page context was incomplete. Answer from general mutual-fund knowledge if the question is mutual-fund related.",
                        intent
                    )
            
            # Extract source documents for citation
            source_docs = [res.get('id', 'unknown') for res in search_results[:2]]
            
            return {
                'response': response_text,
                'source_documents': source_docs,
                'confidence': self._calculate_confidence(search_results),
                'intent': intent,
                'timestamp': datetime.now().isoformat(),
                'model_used': self.model_name if self.model else "local_summarizer"
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'response': "An error occurred while generating the response. Please try again later.",
                'source_documents': [],
                'confidence': 0.0,
                'intent': intent,
                'timestamp': datetime.now().isoformat()
            }

    def _prepare_context(self, results: List[Dict[str, Any]]) -> str:
        """Combine search results into a context string"""
        if not results:
            return ""
        
        context_parts = []
        for i, res in enumerate(results):
            content = res.get('content', '')
            metadata = res.get('metadata', {})
            source = metadata.get('source_url', 'official source')
            
            context_parts.append(f"[Source {i+1}: {source}]\n{content}")
            
        return "\n\n".join(context_parts)

    def _build_context(self, results: List[Dict[str, Any]]) -> str:
        """Build prompt context from retrieved documents plus stable HDFC reference context."""
        retrieved_context = self._prepare_context(results)
        if retrieved_context:
            return f"{retrieved_context}\n\n[Assistant reference]\n{self.hdfc_reference_context}"

        return f"[Assistant reference]\n{self.hdfc_reference_context}"

    def _extract_structured_answer(self, query: str, results: List[Dict[str, Any]]) -> Optional[str]:
        """Extract exact scheme facts from retrieved URL snippets when available."""
        if not results:
            return None

        query_lower = query.lower()
        target_results = self._rank_results_for_query(query_lower, results)
        disclaimer = "Mutual fund investments are subject to market risks. Please read all scheme related documents carefully."

        for result in target_results:
            text = " ".join(result.get("content", "").split())
            metadata = result.get("metadata", {})
            fund_name = metadata.get("fund_name") or self._fund_name_from_source(metadata.get("source_url", ""))

            if ("fund manager" in query_lower or "manager" in query_lower) and "current fund manager" in text.lower():
                manager_match = re.search(r"([A-Z][A-Za-z .]+?)\s+is the Current Fund Manager of\s+(.+?)\s+fund", text)
                if manager_match:
                    manager = manager_match.group(1).strip()
                    scheme = manager_match.group(2).strip()
                    return f"{manager} is listed as the current fund manager of {scheme}. {disclaimer}"

            if "minimum" in query_lower or "sip" in query_lower or "lumpsum" in query_lower:
                sip_match = re.search(r"Minimum SIP Investment is set to\s+(₹[\d,]+)", text)
                lumpsum_match = re.search(r"Minimum Lumpsum Investment is\s+(₹[\d,]+)", text)
                if sip_match or lumpsum_match:
                    parts = []
                    if sip_match:
                        parts.append(f"minimum SIP investment is {sip_match.group(1)}")
                    if lumpsum_match:
                        parts.append(f"minimum lumpsum investment is {lumpsum_match.group(1)}")
                    return f"For {fund_name}, the {', and the '.join(parts)} according to the retrieved fund page. {disclaimer}"

            if "nav" in query_lower:
                nav_match = re.search(r"Latest NAV as of\s+([^.]+?)\s+is\s+(₹[\d,.]+)", text)
                if nav_match:
                    return f"For {fund_name}, the latest NAV shown in the retrieved fund page is {nav_match.group(2)} as of {nav_match.group(1).strip()}. {disclaimer}"

            if "exit load" in query_lower:
                exit_match = re.search(r"Exit load of\s+([^.;]+)", text)
                if exit_match:
                    return f"For {fund_name}, the retrieved fund page states an exit load of {exit_match.group(1).strip()}. {disclaimer}"

            if "risk" in query_lower or "riskometer" in query_lower:
                risk_match = re.search(r"is rated\s+([A-Za-z ]+?)\s+risk", text)
                if risk_match:
                    return f"{fund_name} is shown as {risk_match.group(1).strip()} risk in the retrieved fund page. {disclaimer}"

            if "objective" in query_lower:
                objective_match = re.search(r"Investment Objective The scheme seeks to\s+(.+?)(?: Fund benchmark| Scheme Information|$)", text)
                if objective_match:
                    return f"The investment objective of {fund_name} is to {objective_match.group(1).strip()}. {disclaimer}"

            if "benchmark" in query_lower or "index" in query_lower:
                benchmark_match = re.search(r"Fund benchmark\s+(.+?)(?: Scheme Information| Fund house|$)", text)
                if benchmark_match:
                    return f"The benchmark shown for {fund_name} is {benchmark_match.group(1).strip()}. {disclaimer}"

            if "expense ratio" in query_lower and metadata.get("expense_ratio"):
                return f"For {fund_name}, the expense ratio in the retrieved metadata is {metadata['expense_ratio']}. Please verify the latest figure on the official scheme page. {disclaimer}"

            if ("aum" in query_lower or "assets under management" in query_lower) and metadata.get("aum"):
                return f"For {fund_name}, the retrieved metadata shows AUM as {metadata['aum']}. Please verify the latest figure on the official scheme page. {disclaimer}"

            if "return" in query_lower or "returns" in query_lower or "performance" in query_lower or "performed" in query_lower:
                exact_return = self._extract_return_period_answer(query_lower, text, fund_name, disclaimer)
                if exact_return:
                    return exact_return

        if "return" in query_lower or "returns" in query_lower or "performance" in query_lower or "performed" in query_lower:
            return self._build_missing_performance_answer(query_lower, target_results, disclaimer)

        return None

    def _extract_return_period_answer(self, query_lower: str, text: str, fund_name: str, disclaimer: str) -> Optional[str]:
        """Extract return-period data only when the snippet clearly labels it."""
        periods = []
        if "5" in query_lower or "five" in query_lower:
            periods.append(("5-year", r"(?:5Y|5\s*Y|5\s*Year|5\s*year)[^\d+-]*([+-]?\d+(?:\.\d+)?%)"))
        if "10" in query_lower or "ten" in query_lower:
            periods.append(("10-year", r"(?:10Y|10\s*Y|10\s*Year|10\s*year)[^\d+-]*([+-]?\d+(?:\.\d+)?%)"))
        if "3" in query_lower or "three" in query_lower:
            periods.append(("3-year", r"(?:3Y|3\s*Y|3\s*Year|3\s*year)[^\d+-]*([+-]?\d+(?:\.\d+)?%)"))
        if "1" in query_lower or "one" in query_lower:
            periods.append(("1-year", r"(?:1Y|1\s*Y|1\s*Year|1\s*year)[^\d+-]*([+-]?\d+(?:\.\d+)?%)"))

        found = []
        for label, pattern in periods:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                found.append(f"{label} return: {match.group(1)}")

        if found:
            return f"For {fund_name}, the retrieved fund-page snippet shows {', '.join(found)}. Past performance does not guarantee future returns. {disclaimer}"

        return None

    def _build_missing_performance_answer(self, query_lower: str, results: List[Dict[str, Any]], disclaimer: str) -> str:
        """Give a grounded answer when requested performance periods are absent from retrieved snippets."""
        fund_name = "the requested HDFC fund"
        retrieved_facts = []

        for result in results:
            metadata = result.get("metadata", {})
            text = " ".join(result.get("content", "").split())
            fund_name = metadata.get("fund_name") or self._fund_name_from_source(metadata.get("source_url", "")) or fund_name

            nav_match = re.search(r"Latest NAV as of\s+([^.]+?)\s+is\s+(₹[\d,.]+)", text)
            risk_match = re.search(r"is rated\s+([A-Za-z ]+?)\s+risk", text)
            benchmark_match = re.search(r"Fund benchmark\s+(.+?)(?: Scheme Information| Fund house|$)", text)

            if nav_match:
                retrieved_facts.append(f"NAV {nav_match.group(2)} as of {nav_match.group(1).strip()}")
            if risk_match:
                retrieved_facts.append(f"{risk_match.group(1).strip()} risk")
            if benchmark_match:
                retrieved_facts.append(f"benchmark: {benchmark_match.group(1).strip()}")

            if retrieved_facts:
                break

        requested_periods = []
        if "5" in query_lower or "five" in query_lower:
            requested_periods.append("5-year")
        if "10" in query_lower or "ten" in query_lower:
            requested_periods.append("10-year")
        period_text = " and ".join(requested_periods) if requested_periods else "requested"

        facts_text = f" The retrieved snippet did include {', '.join(retrieved_facts)}." if retrieved_facts else ""
        return (
            f"I could not find clearly labelled {period_text} return figures for {fund_name} in the retrieved snippets, so I should not invent those numbers."
            f"{facts_text} For exact trailing return figures, check the latest HDFC scheme factsheet or official fund page, and compare periods like 1-year, 3-year, 5-year, and 10-year using the same plan and option."
            f" {disclaimer}"
        )

    def _rank_results_for_query(self, query_lower: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prefer snippets from the fund mentioned in the query."""
        fund_slug_hints = {
            "large cap": "hdfc-large-cap",
            "mid cap": "hdfc-mid-cap",
            "equity": "hdfc-equity",
            "flexi": "hdfc-equity",
            "focused": "hdfc-focused",
            "elss": "hdfc-elss",
            "tax saver": "hdfc-elss",
        }

        preferred_slug = None
        for phrase, slug in fund_slug_hints.items():
            if phrase in query_lower:
                preferred_slug = slug
                break

        if not preferred_slug:
            return results

        return sorted(
            results,
            key=lambda res: preferred_slug not in res.get("metadata", {}).get("source_url", "").lower()
        )

    def _fund_name_from_source(self, source_url: str) -> str:
        """Best-effort human name from known Groww URL slugs."""
        source_url = source_url.lower()
        if "hdfc-large-cap" in source_url:
            return "HDFC Large Cap Fund Direct Growth"
        if "hdfc-mid-cap" in source_url:
            return "HDFC Mid Cap Fund Direct Growth"
        if "hdfc-equity" in source_url:
            return "HDFC Equity Fund Direct Growth"
        if "hdfc-focused" in source_url:
            return "HDFC Focused Fund Direct Growth"
        if "hdfc-elss" in source_url:
            return "HDFC ELSS Tax Saver Fund Direct Plan Growth"
        return "the HDFC fund"

    def _generate_with_gemini(self, query: str, context: str, intent: str) -> str:
        """Generate response using Gemini 1.5 Flash"""
        try:
            # Construct prompt
            if intent == "entity_specific":
                prompt = f"{self.system_prompt}\n\nQuery: {query}\nContext: {context}\n\nProvide specific details about the mutual fund or fund concept mentioned. If exact current data is missing, explain the concept and say current figures should be checked in the latest scheme page/documents."
            else:
                prompt = f"{self.system_prompt}\n\nQuery: {query}\nContext: {context}\n\nGenerate a factual educational response. Use the context first; if it is incomplete but the question is mutual-fund related, answer from general mutual-fund knowledge without giving investment advice."
            
            # Generate response with Gemini
            from loguru import logger
            logger.debug(f"Sending prompt to Gemini: {prompt[:500]}...")
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 450,
                },
                request_options={"timeout": 20}
            )
            
            if response.text:
                logger.debug(f"Gemini response: {response.text[:200]}...")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response, falling back to simple generation")
                # Fallback to simple response
                return self._generate_factual_response(context, query)
                
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return self._generate_factual_response(context, query)

    def _generate_factual_response(self, context: str, query: str) -> str:
        """Simple rule-based summarization as fallback"""
        common_response = self._generate_common_faq_response(query)
        if common_response:
            return common_response

        # Take the first sentence of the best match
        if not context:
            return "I'm sorry, no relevant information was found."
            
        # Basic extraction logic: ignore source labels and choose a content sentence.
        cleaned_context = re.sub(r"\[Source \d+: [^\]]+\]\s*", "", context).strip()
        sentences = re.split(r'(?<=[.!?])\s+', cleaned_context)
        content_sentences = [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
            and not sentence.strip().lower().startswith("http")
            and "assistant reference" not in sentence.lower()
        ]
        summary = (content_sentences[0] if content_sentences else "I found related fund-page context, but not enough clearly labelled data to answer that specific question.")
        
        # Add risk disclaimer
        disclaimer = "\n\nNote: Mutual Fund investments are subject to market risks. Please read the offer document carefully before investing."
        
        return f"{summary}{disclaimer}"

    def generate_timeout_fallback(self, query: str, search_results: List[Dict[str, Any]]) -> str:
        """Return a useful answer when the LLM is slow or unavailable."""
        common_response = self._generate_common_faq_response(query)
        if common_response:
            return common_response

        context = self._prepare_context(search_results)
        if context:
            return self._generate_factual_response(context, query)

        return (
            "This appears to be a mutual-fund related question, but I could not retrieve enough scheme-specific context quickly. "
            "Please include the exact HDFC scheme name, such as HDFC Large Cap Fund, HDFC Mid Cap Fund, HDFC Focused Fund, HDFC Equity Fund, or HDFC ELSS Tax Saver Fund, and I can explain the relevant fund concept or scheme detail. "
            "Mutual fund investments are subject to market risks. Please read all scheme related documents carefully."
        )

    def _generate_common_faq_response(self, query: str) -> Optional[str]:
        """Answer common mutual-fund education questions without investment advice."""
        query_lower = query.lower()
        disclaimer = "\n\nMutual fund investments are subject to market risks. Please read all scheme related documents carefully."

        if "nav" in query_lower or "net asset value" in query_lower:
            return (
                "NAV, or Net Asset Value, is the per-unit value of a mutual fund scheme. "
                "It is calculated as the scheme's total assets minus liabilities, divided by the number of units outstanding. "
                "NAV changes with the market value of the securities held by the fund."
                f"{disclaimer}"
            )

        if "equity fund" in query_lower or "equity mutual fund" in query_lower:
            return (
                "An equity fund is a mutual fund scheme that invests primarily in shares of companies. "
                "HDFC Mutual Fund offers equity-oriented schemes such as large-cap, mid-cap, focused, ELSS tax saver, and other equity categories, depending on the scheme objective. "
                "Equity funds can fluctuate with stock markets and are generally meant for investors who understand market risk."
                f"{disclaimer}"
            )

        if "sip" in query_lower or "systematic investment plan" in query_lower:
            return (
                "SIP, or Systematic Investment Plan, is a way to invest a fixed amount in a mutual fund at regular intervals. "
                "It can help spread investments across market levels, but it does not guarantee returns or remove market risk. "
                "Minimum SIP amounts and dates depend on the specific scheme and platform."
                f"{disclaimer}"
            )

        if "expense ratio" in query_lower:
            return (
                "Expense ratio is the annual cost charged by a mutual fund scheme for managing and operating the fund, expressed as a percentage of assets. "
                "It is adjusted in the scheme NAV, so investors do not usually pay it as a separate bill. "
                "For the latest expense ratio, check the current scheme factsheet or official fund page."
                f"{disclaimer}"
            )

        if "exit load" in query_lower:
            return (
                "Exit load is a fee that may apply when mutual fund units are redeemed before a specified holding period. "
                "The rate and period vary by scheme, so the latest scheme document or fund page should be checked before redeeming. "
                "Exit load is separate from market gains or losses."
                f"{disclaimer}"
            )

        if "aum" in query_lower or "assets under management" in query_lower:
            return (
                "AUM, or Assets Under Management, is the total market value of assets managed by a mutual fund scheme or fund house. "
                "AUM changes as investors buy or redeem units and as the value of the scheme portfolio changes. "
                "For the latest AUM of a specific HDFC scheme, check the latest factsheet or official fund page."
                f"{disclaimer}"
            )

        if "risk" in query_lower or "riskometer" in query_lower:
            return (
                "Mutual fund risk describes how much the value of a scheme can fluctuate because of market, credit, interest-rate, liquidity, or concentration factors. "
                "Equity-oriented schemes such as large-cap, mid-cap, focused, and ELSS funds usually carry market risk, and their riskometer level should be checked in the latest scheme documents. "
                "A higher-risk category does not guarantee higher returns."
                f"{disclaimer}"
            )

        if "return" in query_lower or "performance" in query_lower:
            return (
                "Mutual fund returns show how the scheme NAV has changed over a period after accounting for portfolio performance and expenses. "
                "Past performance does not guarantee future results, and returns can vary across time periods and market cycles. "
                "For exact HDFC scheme return figures, check the latest factsheet or official fund page."
                f"{disclaimer}"
            )

        if "minimum" in query_lower or "lumpsum" in query_lower:
            return (
                "Minimum investment is the smallest amount accepted for a mutual fund transaction, and it can differ for SIP and lumpsum purchases. "
                "The exact minimum amount depends on the specific HDFC scheme, plan, option, and transaction platform. "
                "Please verify the latest minimum investment amount on the official scheme page or scheme documents."
                f"{disclaimer}"
            )

        if "fund manager" in query_lower or "manager" in query_lower:
            return (
                "A fund manager is the professional responsible for managing a scheme portfolio according to the scheme objective and investment strategy. "
                "Fund managers can change over time, so the current manager for any HDFC scheme should be checked in the latest factsheet or official scheme page. "
                "Mutual fund investments are subject to market risks. Please read all scheme related documents carefully."
            )

        if "benchmark" in query_lower or "index" in query_lower:
            return (
                "A benchmark is an index used to compare a mutual fund scheme's performance against a relevant market segment. "
                "For example, large-cap, mid-cap, focused, and ELSS schemes may use different equity benchmarks based on their investment universe. "
                "The exact benchmark for a specific HDFC scheme should be checked in the latest scheme document or fund page."
                f"{disclaimer}"
            )

        if "direct" in query_lower or "regular" in query_lower:
            return (
                "Direct and Regular are plan types of a mutual fund scheme. "
                "A Direct plan is usually purchased directly with the fund house or eligible platform and generally has a lower expense ratio, while a Regular plan involves distributor commission and may have a higher expense ratio. "
                "The right plan depends on investor preference and advice needs; compare current scheme documents before investing."
                f"{disclaimer}"
            )

        if "elss" in query_lower or "tax saver" in query_lower:
            return (
                "ELSS, or Equity Linked Savings Scheme, is an equity-oriented mutual fund category that may offer tax benefits under Section 80C, subject to applicable tax rules. "
                "ELSS schemes usually have a statutory lock-in period of three years. "
                "Tax rules can change, so investors should verify the latest rules or consult a tax advisor."
                f"{disclaimer}"
            )

        if "mutual fund" in query_lower and any(word in query_lower for word in ["what", "define", "meaning", "explain"]):
            return (
                "A mutual fund pools money from many investors and invests it in securities such as equities, debt instruments, or money-market instruments according to the scheme objective. "
                "Investors receive units of the scheme, and the value of those units is reflected through the scheme NAV. "
                "Returns are not guaranteed and depend on market performance."
                f"{disclaimer}"
            )

        return None

    def _is_mutual_fund_related(self, query: str) -> bool:
        """Check whether the assistant should answer the question."""
        query_lower = query.lower()
        related_terms = [
            "mutual fund", "hdfc", "fund", "nav", "net asset value", "sip",
            "systematic investment", "expense ratio", "exit load", "aum",
            "return", "risk", "elss", "tax saver", "large cap", "mid cap",
            "equity", "focused", "scheme", "units", "redeem", "redemption",
            "portfolio", "benchmark", "nifty", "groww", "investment",
            "lumpsum", "minimum", "manager", "fund manager", "lock in",
            "lock-in", "tax", "dividend", "growth", "direct", "regular",
            "objective", "holdings", "asset allocation", "factsheet",
            "expense", "ratio", "returns", "performance", "purchase"
        ]

        return any(term in query_lower for term in related_terms)

    def _is_unhelpful_response(self, response_text: str) -> bool:
        """Detect generic no-context responses that can be replaced by safe FAQ answers."""
        if not response_text:
            return True

        response_lower = response_text.lower()
        return (
            "i don't have that information" in response_lower
            or "couldn't find any relevant information" in response_lower
            or "please contact hdfc mutual fund" in response_lower
            or "can only help with mutual-fund related questions" in response_lower
            or "could not retrieve enough" in response_lower
        )

    def _calculate_confidence(self, results: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on similarity scores"""
        if not results:
            return 0.0
            
        scores = [res.get('similarity_score', 0.0) for res in results]
        confidence = sum(scores) / len(scores) if scores else 0.0
        return max(0.0, min(1.0, confidence))
