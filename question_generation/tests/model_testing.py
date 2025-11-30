"""
Code for testing the model ouput and functionality of base question generator module
"""

from ..app.services.question_generator import QuestionGenerator
from ..app.services.helpers.types import ExpRange

if __name__ == "__main__":
    qg = QuestionGenerator('gpt-4.1-mini')
    role = "Software Engineer 1"
    erange = ExpRange(min_exp=1, max_exp=3)
    description = """
        
About the job

Software Development Engineer - 1

Location: Bengaluru/Gurugram (Hybrid)

Reports To: Engineering Manager

Experience: 2–5 years

About GoKwik

GoKwik is a growth operating system designed to power D2C and eCommerce brands from checkout optimization and reducing return-to-origin (RTO), to payments, retention, and post-purchase engagement. Today, GoKwik enables over 12,000 merchants worldwide, processes around $2 billion in GMV, and is strengthening its AI-powered infrastructure.

Backed by RTP Global, Z47, Peak XV, and Think Investments and bolstered by a $13 million growth round in June 2025 (total funding: $68 million) GoKwik is scaling aggressively across India, the UK, Europe, and the US.

Why This Role Matters

As a Customer Success Manager in the Merchant Success Team , you will be responsible to Interact & handle our Merchants/Accounts & leverage data to drive conversion improvements, provide key data-driven insights & indirectly improve GMV of Merchants, Further Customer Success Manager's would be closely working with our Customer Engineering, Technology & Product Team.

Looking for CSMs who are looking to drive a tonne of impact in early stage startups and are excited about seeing their insights translate into actions quickly!

What You’ll Own

    Build and optimize scalable backend systems that power India’s leading eCommerce brands
    Drive the evolution of GoKwik’s core platform with Node.js and high-performance architecture
    Design robust APIs and infrastructure to reduce RTOs and boost conversion rates
    Contribute across the stack—write clean, testable code and implement secure, scalable solutions
    Own end-to-end delivery: from design to deployment, debugging to iteration
    Solve complex challenges in checkout, reliability, data flow, and performance optimisation

Who You Are

    Strong expertise in Node.js and frameworks like Restify
    Solid understanding of REST APIs, server-side templating, and backend business logic
    Comfortable working with Linux systems and Git-based workflows
    Hands-on experience with cloud platforms (AWS, GCP) and container tools (Docker, Kubernetes)
    Basic understanding of front-end technologies (HTML5, CSS3)
    Passionate about building secure, scalable, and maintainable systems
    A self-starter attitude—analytical, adaptable, and ready to work in a fast-paced startup environment.

 

Why GoKwik? 

At GoKwik, we aren’t just building tools — we’re rewriting the playbook for eCommerce in India. We exist to solve some of the most complex challenges faced by digital-first brands: low conversion rates, high RTO, and poor post-purchase experience. Our checkout and conversion stack powers 500+ leading D2C brands and marketplaces — and we’re just getting started.

    """
    res = qg.invoke(role, erange, description)
    print(res)
