config = {
    "harmonic": [
        {
            "description": "Use our enrichment endpoints to get a full picture about companies and people. By passing in a company or person identifier, you'll get back data about teams, financing, social metrics, headcount data, past experiences, and more.",
            "method": "POST",
            "template_call": "https://api.harmonic.ai/companies",
            "query_param": {
                "website_domain": ""
            },
            "headers": {
                "apikey": ""
            }
        },
        {
            "description": "Use our enrichment endpoints to get a full picture about companies and people. By passing in a company or person identifier, you'll get back data about teams, financing, social metrics, headcount data, past experiences, and more.",
            "method": "POST",
            "template_call": "https://api.harmonic.ai/search/similar_companies/:id",
            "query_param": {
                "website_domain": ""
            },
            "interpolations": {
                ":id": ""
            },
            "headers": {
                "apikey": ""
            }
        },
        {
            "description": "Pass in a list of company IDs or URNs, and get back a full picture of those companies. Note: If a company ID is -1, that we means we don't yet have a canonical company record for that company. The API will not return data for these companies. Note: The data in latest company snapshot might not match the current state of the company for up to 14 days. This is because we take snapshot of a company every 14 days but we might update the live state of company before that. ",
            "method": "POST",
            "template_call": "https://api.harmonic.ai/companies/batchGet",
            "query_param": {
                "website_domain": ""
            },
            "interpolations": {
                ":id": ""
            },
            "headers": {
                "apikey": ""
            }
        },
        {
            "description": "This endpoint returns the urns of the employees from a given company.",
            "method": "POST",
            "template_call": "https://api.harmonic.ai/watchlists/people/:id",
            "query_param": {
                "website_domain": ""
            },
            "interpolations": {
                ":id": ""
            },
            "headers": {
                "apikey": ""
            }
        }
    ]
}
