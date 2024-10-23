import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd
import json
import time

st.set_page_config(page_title="Pharmacy Calls Dashboard", page_icon="📞", layout="wide")


def generate_varied_summary():
    # Common elements that can be mixed and matched
    medications = [
        "blood pressure medication", "insulin", "antidepressants", "pain medication",
        "cholesterol medication", "thyroid medication", "antibiotic prescription",
        "asthma inhaler", "anti-anxiety medication", "heart medication"
    ]
    
    situations = [
        "running low on", "lost their", "needs clarification about dosage for",
        "experiencing side effects from", "requesting refill for",
        "concerned about interaction with", "needs prior authorization for",
        "reported adverse reaction to", "seeking alternative to",
        "cannot afford", "missed several doses of"
    ]
    
    urgency_reasons = [
        "due to upcoming travel plans",
        "as current supply will run out tomorrow",
        "due to worsening symptoms",
        "because of insurance expiration",
        "before leaving for vacation",
        "after missing several doses",
        "following doctor's new instructions",
        "due to pharmacy closure",
        "because of adverse reactions",
        ""  # Empty string for cases without urgent reason
    ]
    
    additional_contexts = [
        "Insurance requires documentation.",
        "Previous prescription shows no refills remaining.",
        "Patient reported dizziness as side effect.",
        "Needs copay assistance program information.",
        "Recently switched from different medication.",
        "Requires pharmacist consultation.",
        "Doctor's office needs to be contacted.",
        "Patient has questions about proper storage.",
        "Concerned about drug interactions.",
        "Requesting home delivery options.",
        "Needs Spanish-speaking pharmacist.",
        ""  # Empty string for cases without additional context
    ]

    # Generate the main situation
    main_situation = f"Patient {random.choice(situations)} {random.choice(medications)}"
    
    # Maybe add urgency reason
    if random.random() > 0.3:  # 70% chance to add urgency reason
        urgency = random.choice(urgency_reasons)
        if urgency:
            main_situation += f" {urgency}"
    
    # Maybe add context
    if random.random() > 0.5:  # 50% chance to add context
        context = random.choice(additional_contexts)
        if context:
            main_situation += f" {context}"

    # Determine intent and urgency based on content
    if any(word in main_situation.lower() for word in ["tomorrow", "run out", "missing", "adverse", "worsening"]):
        urgency = "High"
        intent = "Urgent Refill Request"
    elif "side effect" in main_situation.lower() or "adverse" in main_situation.lower():
        urgency = "Medium"
        intent = "Side Effect Report"
    elif "insurance" in main_situation.lower() or "afford" in main_situation.lower():
        urgency = "Medium"
        intent = "Insurance Query"
    else:
        urgency = "Low"
        intent = "General Inquiry"

    # Determine sentiment based on content
    if any(word in main_situation.lower() for word in ["concerned", "adverse", "worsening", "cannot afford"]):
        sentiment = "Anxious"
    elif "urgency" in main_situation.lower() or "tomorrow" in main_situation.lower():
        sentiment = "Urgent"
    else:
        sentiment = random.choice(["Neutral", "Calm", "Inquiring"])

    return {
        "summary": main_situation,
        "intent": intent,
        "urgency": urgency,
        "sentiment": sentiment
    }

def generate_voicemail_message(customer_name):
    # Common voicemail components
    rx_number = f"RX{random.randint(100000, 999999)}"
    medications = [
        "Lisinopril 10mg", "Metformin 1000mg", "Atorvastatin 40mg",
        "Sertraline 50mg", "Levothyroxine 75mcg", "Amoxicillin 500mg",
        "Omeprazole 20mg", "Gabapentin 300mg", "Hydrochlorothiazide 25mg"
    ]
    
    callback_numbers = [
        f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"
        for _ in range(3)
    ]
    
    # Different types of voicemail scenarios
    scenarios = [
        {
            "type": "refill_request",
            "templates": [
                f"Hi, this is {customer_name} calling about my prescription {rx_number} for {random.choice(medications)}. "
                f"I'm running low and need a refill. My number is {random.choice(callback_numbers)}. "
                "Please call me back to let me know when it will be ready.",

                f"Hello, {customer_name} here. I need to refill my {random.choice(medications)}, "
                f"prescription number {rx_number}. I'm down to my last few pills. "
                f"You can reach me at {random.choice(callback_numbers)}. Thank you.",
            ]
        },
        {
            "type": "urgent_request",
            "templates": [
                f"This is {customer_name} and I urgently need my {random.choice(medications)}. "
                f"I'm completely out and it's prescription {rx_number}. "
                f"Please call me as soon as possible at {random.choice(callback_numbers)}. "
                "This is really important.",

                f"Hello, {customer_name} calling. I have an emergency with my prescription {rx_number}. "
                f"I lost my medication bottle of {random.choice(medications)} while traveling. "
                f"Please call me back immediately at {random.choice(callback_numbers)}. "
                "I need this medication daily.",
            ]
        },
        {
            "type": "insurance_query",
            "templates": [
                f"Hi, this is {customer_name}. I'm calling about a problem with my insurance coverage "
                f"for prescription {rx_number}. They're saying it needs prior authorization. "
                f"Please call me back at {random.choice(callback_numbers)} to discuss this.",

                f"Hello, {customer_name} here. I got a message saying there's an insurance issue "
                f"with my {random.choice(medications)}. My number is {random.choice(callback_numbers)}. "
                "I need to know what I need to do to get this resolved.",
            ]
        },
        {
            "type": "side_effect_concern",
            "templates": [
                f"This is {customer_name} calling about my prescription {rx_number} for {random.choice(medications)}. "
                "I'm experiencing some side effects and need to speak with a pharmacist. "
                f"My callback number is {random.choice(callback_numbers)}.",

                f"Hi, {customer_name} here. I've been having some reactions to my new prescription "
                f"{rx_number} and need to discuss this with someone. Please call me at "
                f"{random.choice(callback_numbers)}. I'm concerned about continuing the medication.",
            ]
        },
        {
            "type": "transfer_request",
            "templates": [
                f"Hello, this is {customer_name}. I need to transfer my prescriptions from another pharmacy. "
                f"I have about 5 medications including {random.choice(medications)}. "
                f"Please call me back at {random.choice(callback_numbers)} to help with this process.",

                f"Hi, {customer_name} calling about transferring my medications to your pharmacy. "
                f"My current prescription number is {rx_number}. You can reach me at {random.choice(callback_numbers)}. "
                "I'd like to get this started as soon as possible.",
            ]
        },
        {
            "type": "cost_concern",
            "templates": [
                f"Hi, this is {customer_name} calling about the cost of my prescription {rx_number}. "
                f"The price seems much higher than usual for my {random.choice(medications)}. "
                f"Please call me back at {random.choice(callback_numbers)} to discuss any discount options.",

                f"Hello, {customer_name} here. I'm having trouble affording my prescription and "
                "wanted to know if there are any cheaper alternatives or discount programs available. "
                f"My number is {random.choice(callback_numbers)}.",
            ]
        }
    ]
    
    # Select a random scenario and template
    scenario = random.choice(scenarios)
    message = random.choice(scenario["templates"])
    
    # Add common voicemail endings
    endings = [
        " Thanks for your help.",
        " Please call me back when you can.",
        " I appreciate your help with this.",
        " Looking forward to hearing back from you.",
        " Please let me know as soon as possible."
    ]
    
    times_to_call = [
        "I'm available anytime today.",
        "Best time to reach me is in the afternoon.",
        "Please call before 5pm if possible.",
        "I'm available between 9am and 6pm.",
        "You can call me back anytime.",
        ""  # Empty string for cases where no time preference is given
    ]
    
    message += random.choice(endings)
    if random.random() > 0.5:  # 50% chance to add time preference
        message += " " + random.choice(times_to_call)

    return {
        "voicemail_type": scenario["type"],
        "message": message,
        "timestamp": datetime.now() - timedelta(minutes=random.randint(5, 120)),
        "duration": f"{random.randint(20, 90)} seconds",
        "callback_number": random.choice(callback_numbers),
        "prescription_mentioned": rx_number if "rx_number" in message else None,
        "urgent": scenario["type"] == "urgent_request",
        "requires_pharmacist": scenario["type"] in ["side_effect_concern", "urgent_request"],
        "call_back_preference": random.choice([
            "Morning", "Afternoon", "Evening", "ASAP", "Any time"
        ]),
        "auto_transcription_confidence": random.randint(85, 99)
    }

def generate_sample_calls(n_calls=10):
    customers = [
        "Sarah Johnson", "Mike Smith", "Emily Brown", "James Wilson", 
        "Maria Garcia", "David Lee", "Lisa Anderson", "Robert Taylor", 
        "Jennifer Martinez", "William Davis", "Emma Thompson", "John Carter",
        "Patricia Rodriguez", "Michael Chang", "Susan Miller"
    ]
    
    calls = []
    for _ in range(n_calls):
        customer_name = random.choice(customers)
        voicemail = generate_voicemail_message(customer_name)
        analysis = generate_enhanced_call_analysis()
        
        call = {
            "call_id": f"CALL-{2024}{random.randint(1000, 9999)}",
            "customer_name": customer_name,
            "timestamp": voicemail["timestamp"],
            "duration": voicemail["duration"],
            "category": voicemail["voicemail_type"].replace("_", " ").title(),
            "status": "Urgent" if voicemail["urgent"] else random.choice(["New", "Pending", "In Progress"]),
            "callback_required": True,  # All voicemails require callbacks
            "prescriptions_discussed": 1 if voicemail["prescription_mentioned"] else 0,
            "voicemail_data": voicemail,
            "metadata": generate_call_metadata(),
            "analysis": analysis
        }
        calls.append(call)
    
    return calls

def generate_call_analysis():
    scenario = generate_varied_summary()
    similar_cases = [
        {
            "case_id": f"CASE-{random.randint(1000, 9999)}",
            "similarity": random.randint(75, 95),
            "resolution": random.choice([
                "Processed emergency refill and contacted doctor",
                "Provided copay assistance information",
                "Scheduled pharmacist consultation",
                "Transferred prescription to new location",
                "Contacted insurance for prior authorization",
                "Applied discount card to reduce cost",
                "Documented side effects and notified doctor",
                "Arranged home delivery service",
                "Provided medication interaction review",
                "Completed insurance override request"
            ])
        }
        for _ in range(random.randint(2, 4))
    ]
    
    # Generate relevant key phrases based on the summary
    possible_phrases = [
        "medication shortage", "insurance coverage", "side effects", "urgent refill",
        "prior authorization", "drug interaction", "vacation override", "lost medication",
        "dosing schedule", "adverse reaction", "insurance denial", "travel emergency",
        "copay assistance", "pharmacy transfer", "home delivery", "consultation required",
        "doctor notification", "prescription expired", "language assistance", "payment plan"
    ]
    
    # Select phrases that are relevant to the summary
    relevant_phrases = [phrase for phrase in possible_phrases 
                       if any(word in scenario["summary"].lower() for word in phrase.split())]
    
    # Add some random phrases if we don't have enough relevant ones
    if len(relevant_phrases) < 3:
        additional_phrases = random.sample([p for p in possible_phrases if p not in relevant_phrases],
                                        k=min(3, len(possible_phrases) - len(relevant_phrases)))
        relevant_phrases.extend(additional_phrases)
    
    return {
        "call_summary": scenario["summary"],
        "primary_intent": scenario["intent"],
        "confidence_score": random.randint(85, 99),
        "urgency_level": scenario["urgency"],
        "sentiment": scenario["sentiment"],
        "similar_cases": similar_cases,
        "key_phrases": random.sample(relevant_phrases, k=min(len(relevant_phrases), 4))
    }



def generate_sample_transcript(customer_name):
    rx_number = f"RX{random.randint(100000, 999999)}"
    medications = ["Amoxicillin 500mg", "Lisinopril 10mg", "Metformin 1000mg", "Sertraline 50mg", "Omeprazole 20mg"]
    selected_med = random.choice(medications)
    
    return {
        "automated_system": "Thank you for calling CVS Pharmacy. For prescription refills, press 1. Para español, presione 2.",
        "customer": f"Hi, this is {customer_name}. I need to refill my prescription {rx_number}.",
        "pharmacist": f"Hello {customer_name}, I can help you with that. I see your prescription for {selected_med}. When would you like to pick this up?",
        "customer_response": "Can I get it today? I'm running low on my medication.",
        "pharmacist_closing": f"Yes, I can have that ready in about 2 hours. We'll send you a text message when it's ready. Is there anything else I can help you with?",
        "customer_closing": "No, that's all. Thank you for your help!"
    }

def generate_call_metadata():
    departments = ["Pharmacy", "Insurance", "Medical Review", "Customer Service", "Clinical Support"]
    priorities = ["High", "Medium", "Low"]
    ticket_types = ["Medication Issue", "Insurance Claim", "Prescription Renewal", "Side Effect Report", "Drug Interaction"]
    
    return {
        "ticket_id": f"TKT-{random.randint(10000, 99999)}",
        "department": random.choice(departments),
        "priority": random.choice(priorities),
        "ticket_type": random.choice(ticket_types),
        "assigned_to": f"Agent-{random.randint(100, 999)}",
        "sla_hours": random.choice([2, 4, 8, 24, 48]),
        "tags": random.sample(["#urgent", "#callback", "#prescription", "#insurance", "#review", "#followup"], 
                            k=random.randint(2, 4))
    }



def analyze_intent(transcript):
    # Extract conversation text
    customer_text = transcript['customer'] + " " + transcript['customer_response']
    
    # Keywords for different intents
    intent_keywords = {
        "Urgent Refill Request": ["today", "running low", "need", "refill", "emergency", "urgent", "out of"],
        "General Refill": ["refill", "prescription", "medication", "renew"],
        "Side Effect Report": ["side effect", "reaction", "feeling", "dizzy", "sick", "pain"],
        "Insurance Query": ["insurance", "coverage", "cost", "pay", "price"],
        "Drug Information": ["information", "how to", "when", "effects", "instructions"],
        "Prescription Transfer": ["transfer", "move", "different", "another", "pharmacy"],
        "Medication Inquiry": ["about", "question", "ask", "explain", "understand"],
    }

def generate_enhanced_call_analysis():
    # Generate more detailed sentiment analysis
    sentiment_analysis = {
        "primary_emotion": random.choice([
            "Anxious", "Frustrated", "Satisfied", "Confused", 
            "Urgent", "Neutral", "Concerned", "Appreciative"
        ]),
        "secondary_emotions": random.sample([
            "Worried about cost", "Uncertain about instructions",
            "Relieved about solution", "Stressed about timeline",
            "Grateful for help", "Confused about process"
        ], k=2),
        "confidence_score": random.randint(85, 99),
        "emotion_triggers": random.sample([
            "medication cost", "insurance coverage",
            "side effects", "waiting time",
            "prescription availability", "doctor approval"
        ], k=2)
    }

    # Generate compliance and risk indicators
    risk_assessment = {
        "risk_level": random.choice(["Low", "Medium", "High"]),
        "risk_factors": random.sample([
            "Missed doses", "Drug interaction potential",
            "Side effect concerns", "Delayed refill",
            "Insurance expiration", "Multiple pharmacy usage"
        ], k=random.randint(1, 3)),
        "compliance_score": random.randint(60, 100),
        "adherence_patterns": random.choice([
            "Regular refills", "Occasional delays",
            "Frequent missed doses", "Inconsistent pickup"
        ])
    }

    # Generate action items and recommendations
    action_items = []
    possible_actions = [
        {
            "action": "Schedule follow-up call",
            "priority": "High",
            "deadline": "24 hours",
            "reason": "Discuss side effects"
        },
        {
            "action": "Contact prescribing physician",
            "priority": "Medium",
            "deadline": "48 hours",
            "reason": "Verify dosage change"
        },
        {
            "action": "Process prior authorization",
            "priority": "High",
            "deadline": "24 hours",
            "reason": "Insurance requirement"
        },
        {
            "action": "Update patient profile",
            "priority": "Low",
            "deadline": "72 hours",
            "reason": "New contact information"
        },
        {
            "action": "Schedule medication review",
            "priority": "Medium",
            "deadline": "48 hours",
            "reason": "Multiple medication interactions"
        }
    ]
    action_items = random.sample(possible_actions, k=random.randint(1, 3))

    # Generate regulatory compliance check
    compliance_check = {
        "hipaa_compliant": True,
        "phi_disclosed": random.choice([True, False]),
        "required_disclaimers_given": random.choice([True, False]),
        "consent_verified": random.choice([True, False]),
        "documentation_complete": random.choice([True, False])
    }

    # Generate call quality metrics
    call_quality = {
        "clarity_score": random.randint(80, 100),
        "resolution_completeness": random.randint(70, 100),
        "customer_satisfaction_predicted": random.randint(60, 100),
        "follow_up_needed": random.choice([True, False]),
        "escalation_required": random.choice([True, False])
    }

    # Generate key topics and themes
    topics_identified = random.sample([
        "Prescription Renewal", "Insurance Coverage",
        "Side Effects", "Drug Interactions",
        "Payment Concerns", "Delivery Options",
        "Dosage Instructions", "Generic Alternatives",
        "Prior Authorization", "Pharmacy Transfer"
    ], k=random.randint(2, 4))

    # Generate historical context analysis
    historical_context = {
        "previous_interactions": random.randint(0, 5),
        "common_issues": random.sample([
            "Regular early refill requests",
            "Frequent insurance queries",
            "Multiple medication adjustments",
            "Consistent payment concerns",
            "Regular side effect reports"
        ], k=random.randint(1, 2)),
        "patient_profile_flags": random.sample([
            "Chronic condition",
            "Multiple prescribers",
            "Complex medication regimen",
            "Special handling required",
            "Preferred language support"
        ], k=random.randint(1, 2))
    }

    # Generate AI recommendations
    ai_recommendations = {
        "immediate_actions": random.sample([
            "Process emergency refill",
            "Schedule pharmacist consultation",
            "Contact prescribing physician",
            "Update insurance information",
            "Document reported side effects"
        ], k=random.randint(1, 2)),
        "long_term_suggestions": random.sample([
            "Enroll in auto-refill program",
            "Schedule regular medication review",
            "Consider medication synchronization",
            "Recommend patient assistance program",
            "Set up medication reminders"
        ], k=random.randint(1, 2))
    }

    return {
        "sentiment_analysis": sentiment_analysis,
        "risk_assessment": risk_assessment,
        "action_items": action_items,
        "compliance_check": compliance_check,
        "call_quality": call_quality,
        "topics_identified": topics_identified,
        "historical_context": historical_context,
        "ai_recommendations": ai_recommendations,
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis_version": "2.0.0"
    }

def create_ai_analysis_flow(selected_call):
    st.markdown("## 🤖 Call Analysis")
    
    # Display voicemail instead of transcript
    st.markdown("### 📝 Voicemail Message")
    voicemail = selected_call['voicemail_data']
    
    # Display voicemail details in a structured way
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Message:**")
            st.markdown(f"_{voicemail['message']}_")
        with col2:
            st.markdown("**Details:**")
            st.markdown(f"Duration: {voicemail['duration']}")
            st.markdown(f"Callback #: {voicemail['callback_number']}")
            st.markdown(f"Preferred Time: {voicemail['call_back_preference']}")
            if voicemail['urgent']:
                st.error("⚠️ Marked as Urgent")
            if voicemail['requires_pharmacist']:
                st.warning("👩‍⚕️ Requires Pharmacist")
    st.markdown("---")
    # Initial state - show analyze button
    if st.session_state.analysis_stage == 'initial':
        if st.button("🔍 Analyze Voice Mail", key=f"analyze_transcript_{selected_call['call_id']}", type="primary"):
            st.session_state.analysis_stage = 'analyzing'
            st.rerun()

    # Analysis in progress
    elif st.session_state.analysis_stage == 'analyzing':
        status = st.status("🔄 Analysis in Progress...", expanded=True)
        with status:
            # Generate enhanced analysis
            enhanced_analysis = generate_enhanced_call_analysis()
            
            # Show processing steps
            st.write("🎯 Initializing analysis pipeline...")
            time.sleep(0.5)
            
            st.write("🧠 Processing language understanding...")
            time.sleep(1)
            
            st.write("📊 Analyzing sentiment patterns...")
            time.sleep(0.5)
            st.info(f"**Primary Emotion Detected:** {enhanced_analysis['sentiment_analysis']['primary_emotion']}")
            
            st.write("⚠️ Evaluating risk factors...")
            time.sleep(0.7)
            st.warning(f"**Risk Level:** {enhanced_analysis['risk_assessment']['risk_level']}")
            
            st.write("📋 Generating compliance report...")
            time.sleep(0.8)
            
            st.write("🔍 Analyzing historical context...")
            time.sleep(0.6)
            
            st.write("📝 Formulating recommendations...")
            time.sleep(1)
            
            st.session_state.enhanced_analysis = enhanced_analysis
            st.session_state.analysis_stage = 'show_results'
            status.update(label="✅ Analysis Complete!", state="complete")
            st.rerun()

    # Show analysis results
    elif st.session_state.analysis_stage == 'show_results':
        enhanced_analysis = st.session_state.enhanced_analysis
        
        # Display sentiment and emotion analysis
        st.success("### 😊 Sentiment Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Primary Emotion", enhanced_analysis['sentiment_analysis']['primary_emotion'])
            st.markdown("**Emotion Triggers:**")
            for trigger in enhanced_analysis['sentiment_analysis']['emotion_triggers']:
                st.markdown(f"- {trigger}")
        with col2:
            st.metric("Confidence Score", f"{enhanced_analysis['sentiment_analysis']['confidence_score']}%")
            st.markdown("**Secondary Emotions:**")
            for emotion in enhanced_analysis['sentiment_analysis']['secondary_emotions']:
                st.markdown(f"- {emotion}")

        # Display risk assessment
        st.warning("### ⚠️ Risk Assessment")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Risk Level", enhanced_analysis['risk_assessment']['risk_level'])
            st.metric("Compliance Score", f"{enhanced_analysis['risk_assessment']['compliance_score']}%")
        with col2:
            st.markdown("**Risk Factors:**")
            for factor in enhanced_analysis['risk_assessment']['risk_factors']:
                st.markdown(f"- {factor}")
            st.markdown(f"**Adherence Pattern:** {enhanced_analysis['risk_assessment']['adherence_patterns']}")

        # Display action items
        st.info("### 📋 Required Actions")
        for item in enhanced_analysis['action_items']:
            with st.container():
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    st.markdown(f"**{item['action']}**")
                    st.markdown(f"_{item['reason']}_")
                with col2:
                    st.markdown(f"Priority: **{item['priority']}**")
                with col3:
                    st.markdown(f"Deadline: **{item['deadline']}**")

        # Display recommendations
        st.success("### 💡 AI Recommendations")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Immediate Actions:**")
            for action in enhanced_analysis['ai_recommendations']['immediate_actions']:
                st.markdown(f"- {action}")
        with col2:
            st.markdown("**Long-term Suggestions:**")
            for suggestion in enhanced_analysis['ai_recommendations']['long_term_suggestions']:
                st.markdown(f"- {suggestion}")

        # Display call quality metrics
        st.info("### 📊 Call Quality Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Clarity Score", f"{enhanced_analysis['call_quality']['clarity_score']}%")
        with col2:
            st.metric("Resolution Score", f"{enhanced_analysis['call_quality']['resolution_completeness']}%")
        with col3:
            st.metric("Satisfaction Score", f"{enhanced_analysis['call_quality']['customer_satisfaction_predicted']}%")

        # Display compliance check
        if st.checkbox("Show Compliance Details"):
            st.warning("### 🔒 Compliance Check")
            compliance = enhanced_analysis['compliance_check']
            cols = st.columns(3)
            with cols[0]:
                st.markdown("✅ HIPAA Compliant" if compliance['hipaa_compliant'] else "❌ HIPAA Review Needed")
            with cols[1]:
                st.markdown("✅ PHI Properly Handled" if not compliance['phi_disclosed'] else "⚠️ PHI Disclosed")
            with cols[2]:
                st.markdown("✅ Consent Verified" if compliance['consent_verified'] else "❌ Consent Missing")

        # Option to generate ticket
        if st.button("✅ Generate Support Ticket", type="primary", key=f"generate_ticket_{selected_call['call_id']}"):
            st.session_state.analysis_stage = 'ticket_generated'
            st.rerun()

    # Show generated ticket
    elif st.session_state.analysis_stage == 'ticket_generated':
        st.success("### ✅ Support Ticket Generated")
        enhanced_analysis = st.session_state.enhanced_analysis
        
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
        
        # Display ticket details
        st.code(f"""
Ticket ID: {ticket_id}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: Active
Priority: {enhanced_analysis['risk_assessment']['risk_level']}
Risk Level: {enhanced_analysis['risk_assessment']['risk_level']}
Required Actions: {len(enhanced_analysis['action_items'])}
Compliance Score: {enhanced_analysis['risk_assessment']['compliance_score']}%
Follow-up Required: {"Yes" if enhanced_analysis['call_quality']['follow_up_needed'] else "No"}

Primary Concerns:
{chr(10).join(f"- {topic}" for topic in enhanced_analysis['topics_identified'])}

Immediate Actions Required:
{chr(10).join(f"- {action}" for action in enhanced_analysis['ai_recommendations']['immediate_actions'])}
        """)
        
        if st.button("🔄 Start New Analysis", key=f"new_analysis_{selected_call['call_id']}"):
            st.session_state.analysis_stage = 'initial'
            st.rerun()

def generate_sample_calls(n_calls=10):
    customers = [
        "Sarah Johnson", "Mike Smith", "Emily Brown", "James Wilson", 
        "Maria Garcia", "David Lee", "Lisa Anderson", "Robert Taylor", 
        "Jennifer Martinez", "William Davis", "Emma Thompson", "John Carter",
        "Patricia Rodriguez", "Michael Chang", "Susan Miller"
    ]
    
    calls = []
    for _ in range(n_calls):
        customer_name = random.choice(customers)
        voicemail = generate_voicemail_message(customer_name)
        analysis = generate_enhanced_call_analysis()
        
        # Extract just the number from the duration string (e.g., "45 seconds" -> 45)
        duration_seconds = int(voicemail["duration"].split()[0])
        
        call = {
            "call_id": f"CALL-{2024}{random.randint(1000, 9999)}",
            "customer_name": customer_name,
            "timestamp": voicemail["timestamp"],
            "duration_seconds": duration_seconds,  # Store the duration in seconds
            "duration_display": voicemail["duration"],  # Store the display format
            "category": voicemail["voicemail_type"].replace("_", " ").title(),
            "status": "Urgent" if voicemail["urgent"] else random.choice(["New", "Pending", "In Progress"]),
            "callback_required": True,  # All voicemails require callbacks
            "prescriptions_discussed": 1 if voicemail["prescription_mentioned"] else 0,
            "voicemail_data": voicemail,
            "metadata": generate_call_metadata(),
            "analysis": analysis
        }
        calls.append(call)
    
    return calls

# Modified dashboard metrics calculation
def calculate_dashboard_metrics(calls):
    total_calls = len(calls)
    urgent_calls = len([c for c in calls if c["status"] == "Urgent"])
    callbacks_needed = len([c for c in calls if c["callback_required"]])
    
    # Calculate average duration in minutes from seconds
    total_seconds = sum(c["duration_seconds"] for c in calls)
    avg_minutes = round(total_seconds / (total_calls * 60), 1) if total_calls > 0 else 0
    
    return {
        "total_calls": total_calls,
        "urgent_calls": urgent_calls,
        "callbacks_needed": callbacks_needed,
        "avg_duration_minutes": avg_minutes
    }


# Initialize session states at the start
if 'static_calls' not in st.session_state:
    st.session_state.static_calls = generate_sample_calls()

if 'show_ai_analysis' not in st.session_state:
    st.session_state.show_ai_analysis = False

if 'selected_call' not in st.session_state:
    st.session_state.selected_call = None

if 'analysis_stage' not in st.session_state:
    st.session_state.analysis_stage = 'initial'


# Clear cache button
if st.button("🔄 Clear Cache and Reload", key="clear_cache_button"):
    st.cache_data.clear()
    st.session_state.static_calls = generate_sample_calls()
    st.session_state.show_ai_analysis = False
    st.session_state.selected_call = None
    st.session_state.analysis_stage = 'initial'
    st.rerun()

# Dashboard title
st.title("📞 Daily Voicemails")

# Calculate metrics
total_calls = len(st.session_state.static_calls)
urgent_calls = len([c for c in st.session_state.static_calls if c["status"] == "Urgent"])
total_duration_seconds = sum(c.get("duration_seconds", 0) for c in st.session_state.static_calls)
avg_minutes = round(total_duration_seconds / (total_calls * 60), 1) if total_calls > 0 else 0
callbacks = len([c for c in st.session_state.static_calls if c["callback_required"]])

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Voicemails", total_calls)
with col2:
    st.metric("Urgent Cases", urgent_calls)
with col3:
    st.metric("Average Duration", f"{avg_minutes} mins")
with col4:
    st.metric("Pending Callbacks", callbacks)

# Display voicemails
st.markdown("### Recent Voicemails")

for call in sorted(st.session_state.static_calls, key=lambda x: x['timestamp'], reverse=True):
    with st.container():
        st.markdown("---")
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.write(f"**{call['call_id']} - {call['customer_name']}**")
            st.write(f"_{call['voicemail_data']['message']}_")
        
        with col2:
            st.write(f"Time: {call['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            st.write(f"Duration: {call['duration_display']}")
        
        with col3:
            status_color = "🔴" if call['status'] == "Urgent" else "🟡" if call['status'] == "Pending" else "🟢"
            st.write(f"Status: {status_color} {call['status']}")
            st.write(f"Category: {call['category']}")
            if call['voicemail_data']['urgent']:
                st.error("⚠️ URGENT")
        
        with col4:
            if st.button("🔍 Analyze", key=f"analyze_button_{call['call_id']}"):
                st.session_state.selected_call = call
                st.session_state.analysis_stage = 'initial'
        
        # Show analysis section if needed
        if (st.session_state.show_ai_analysis or 
            (st.session_state.selected_call and st.session_state.selected_call['call_id'] == call['call_id'])):
            st.markdown("---")
            create_ai_analysis_flow(call)

# Function to reset session state
def reset_session_state():
    st.session_state.show_ai_analysis = False
    st.session_state.selected_call = None
    st.session_state.analysis_stage = 'initial'
    st.session_state.static_calls = generate_sample_calls()

# Add a footer
st.markdown("---")
st.markdown("### 📊 Dashboard Statistics")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Total Duration:** {total_duration_seconds // 60} minutes")
    st.markdown(f"**Average Message Length:** {avg_minutes} minutes")
with col2:
    st.markdown(f"**Urgent Messages:** {urgent_calls} ({round(urgent_calls/total_calls * 100, 1)}%)")
    st.markdown(f"**Callbacks Required:** {callbacks} ({round(callbacks/total_calls * 100, 1)}%)")

# Optional: Add filtering and sorting controls
if st.checkbox("Show Filtering Options"):
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            ["Urgent", "Pending", "New", "In Progress"],
            default=["Urgent", "Pending", "New", "In Progress"]
        )
    with col2:
        category_filter = st.multiselect(
            "Filter by Category",
            list(set(call['category'] for call in st.session_state.static_calls)),
            default=list(set(call['category'] for call in st.session_state.static_calls))
        )
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            ["Timestamp (Newest)", "Timestamp (Oldest)", "Duration", "Priority"]
        )