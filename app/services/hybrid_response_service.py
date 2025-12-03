# File: app/services/hybrid_response_service.py
"""
Hybrid Response System - Web Scraping + KB + AI Fallback
যখন OpenAI API fail হয়, KB থেকে সরাসরি dynamic answer দেয়
"""

import json
from typing import Dict, List, Optional
from app.logger import logger
from app.services.kb_service import kb_service


class HybridResponseService:
    """
    তিন ধাপে answer generate করে:
    1. KB থেকে semantic match করে answer খুঁজে
    2. যদি match থাকে, KB থেকে dynamic answer তৈরি করে
    3. যদি না থাকে, default answer দেয়
    """

    def __init__(self):
        self.kb_service = kb_service
        self.intent_responses = {
            "general": self._generate_general_response,
            "order_status": self._generate_order_response,
            "refund": self._generate_refund_response,
            "shipping": self._generate_shipping_response,
            "subscription": self._generate_subscription_response,
            "pricing": self._generate_pricing_response,
            "safety": self._generate_safety_response,
            "usage": self._generate_usage_response,
        }

    def get_response(self, message: str, intent: str) -> str:
        """মূল method - intent অনুযায়ী response generate করে"""
        try:
            # KB থেকে relevant items খুঁজে
            kb_results = self.kb_service.search(message, top_k=3)
            
            if kb_results:
                logger.info(f"KB found {len(kb_results)} matches for intent: {intent}")
                return self._build_response_from_kb(message, intent, kb_results)
            else:
                logger.info(f"No KB match, using default response for intent: {intent}")
                return self._get_default_response(intent)
                
        except Exception as e:
            logger.error(f"Error in hybrid response: {e}")
            return self._get_default_response(intent)

    def _build_response_from_kb(self, message: str, intent: str, kb_results: List[Dict]) -> str:
        """KB results থেকে structured response তৈরি করে"""
        
        if intent in self.intent_responses:
            return self.intent_responses[intent](message, kb_results)
        
        return self._generate_general_response(message, kb_results)

    def _generate_general_response(self, message: str, kb_results: List[Dict]) -> str:
        """সাধারণ প্রশ্নের উত্তর"""
        if not kb_results:
            return "আমি HardChews সম্পর্কে আরও তথ্য প্রদান করতে পারি। কি জানতে চান?"
        
        # প্রথম result থেকে extract করে
        top_result = kb_results[0]
        title = top_result.get("title", "")
        content = top_result.get("content", "")
        
        # Friendly response structure
        if "product" in title.lower():
            response = f"{content[:200]}..."
            if len(kb_results) > 1:
                response += f"\n\nআরও তথ্য: {kb_results[1].get('title', '')}"
            return response
        
        return f"{title}\n\n{content}"

    def _generate_usage_response(self, message: str, kb_results: List[Dict]) -> str:
        """কিভাবে ব্যবহার করতে হয়"""
        if not kb_results:
            return "HardChews ব্যবহারের জন্য প্যাকেজিং এর নির্দেশনা অনুসরণ করুন।"
        
        for result in kb_results:
            if "usage" in result.get("title", "").lower() or "dosage" in result.get("title", "").lower():
                return f"✓ {result.get('title')}\n\n{result.get('content', '')}"
        
        # Default যদি specific usage না পাওয়া যায়
        return f"{kb_results[0].get('title')}: {kb_results[0].get('content')}"

    def _generate_refund_response(self, message: str, kb_results: List[Dict]) -> str:
        """রিফান্ড পলিসি"""
        if not kb_results:
            return "আমাদের রিফান্ড পলিসি সম্পর্কে জানতে আমাদের সাথে যোগাযোগ করুন।"
        
        for result in kb_results:
            if "refund" in result.get("title", "").lower():
                return f"💰 {result.get('title')}\n\n{result.get('content', '')}"
        
        return f"{kb_results[0].get('title')}: {kb_results[0].get('content')}"

    def _generate_shipping_response(self, message: str, kb_results: List[Dict]) -> str:
        """শিপিং সম্পর্কে তথ্য"""
        if not kb_results:
            return "শিপিং সম্পর্কে আরও তথ্যের জন্য আমাদের যোগাযোগ করুন।"
        
        for result in kb_results:
            if "shipping" in result.get("title", "").lower() or "delivery" in result.get("title", "").lower():
                return f"📦 {result.get('title')}\n\n{result.get('content', '')}"
        
        return f"{kb_results[0].get('title')}: {kb_results[0].get('content')}"

    def _generate_pricing_response(self, message: str, kb_results: List[Dict]) -> str:
        """মূল্য সম্পর্কিত প্রশ্ন"""
        if not kb_results:
            return "মূল্য সম্পর্কে বর্তমান তথ্য পেতে আমাদের সাথে যোগাযোগ করুন।"
        
        for result in kb_results:
            if "price" in result.get("title", "").lower() or "cost" in result.get("title", "").lower():
                return f"💵 {result.get('title')}\n\n{result.get('content', '')}"
        
        return f"{kb_results[0].get('title')}: {kb_results[0].get('content')}"

    def _generate_safety_response(self, message: str, kb_results: List[Dict]) -> str:
        """নিরাপত্তা এবং সতর্কতা সম্পর্কে"""
        if not kb_results:
            return "নিরাপত্তা সম্পর্কে আরও তথ্যের জন্য চিকিৎসকের সাথে পরামর্শ করুন।"
        
        response_text = "⚠️ **নিরাপত্তা তথ্য**\n\n"
        
        for result in kb_results:
            if "safe" in result.get("title", "").lower() or "side effect" in result.get("title", "").lower():
                response_text += f"{result.get('title')}\n{result.get('content', '')}\n\n"
        
        if response_text == "⚠️ **নিরাপত্তা তথ্য**\n\n":
            response_text = f"{kb_results[0].get('title')}: {kb_results[0].get('content')}"
        
        return response_text

    def _generate_subscription_response(self, message: str, kb_results: List[Dict]) -> str:
        """সাবস্ক্রিপশন সম্পর্কে তথ্য"""
        if not kb_results:
            return "সাবস্ক্রিপশন অপশন সম্পর্কে আরও জানতে যোগাযোগ করুন।"
        
        for result in kb_results:
            if "subscription" in result.get("title", "").lower() or "auto" in result.get("title", "").lower():
                return f"🔄 {result.get('title')}\n\n{result.get('content', '')}"
        
        return f"{kb_results[0].get('title')}: {kb_results[0].get('content')}"

    def _generate_order_response(self, message: str, kb_results: List[Dict]) -> str:
        """অর্ডার স্ট্যাটাস এবং ট্র্যাকিং"""
        response = "📦 **আপনার অর্ডার সম্পর্কে তথ্য**\n\n"
        
        # KB থেকে relevant তথ্য খুঁজে
        found_info = False
        for result in kb_results:
            if "order" in result.get("title", "").lower() or "track" in result.get("title", "").lower():
                response += f"{result.get('title')}\n{result.get('content', '')}\n\n"
                found_info = True
        
        if not found_info and kb_results:
            response += f"আমরা আপনার অর্ডার ট্র্যাক করতে সাহায্য করব। অর্ডার নম্বর এবং ইমেইল সরবরাহ করুন।\n\n"
            response += f"সম্পর্কিত: {kb_results[0].get('title')}"
        
        return response

    def _get_default_response(self, intent: str) -> str:
        """Default fallback responses"""
        defaults = {
            "general": "🤖 আমি HardChews সম্পর্কে সাহায্য করতে এখানে আছি। কোন বিশেষ প্রশ্ন আছে?",
            "order_status": "📦 অর্ডার স্ট্যাটাস জানতে অর্ডার নম্বর এবং ইমেইল দিন।",
            "refund": "💰 আমাদের কাছে একটি সন্তুষ্টি গ্যারান্টি রয়েছে। বিস্তারিতের জন্য যোগাযোগ করুন।",
            "shipping": "📦 শিপিং সময় সম্পর্কে আমাদের যোগাযোগ করুন।",
            "subscription": "🔄 আমরা সুবিধাজনক সাবস্ক্রিপশন অপশন অফার করি।",
            "pricing": "💵 সর্বশেষ মূল্য জানতে আমাদের ওয়েবসাইট দেখুন।",
            "safety": "⚠️ নিরাপত্তা সম্পর্কে প্রশ্নের জন্য চিকিৎসকের সাথে পরামর্শ করুন।",
            "usage": "📋 ব্যবহারের নির্দেশনা প্যাকেজে পাওয়া যায়।",
        }
        return defaults.get(intent, "আপনার প্রশ্নের জন্য ধন্যবাদ। আরও সাহায্যের জন্য যোগাযোগ করুন।")


# Singleton instance
hybrid_service = HybridResponseService()
