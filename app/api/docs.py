from fastapi.openapi.utils import get_openapi
from typing import Dict

from sqlalchemy import true


def custom_openapi(app) -> Dict:
    """Generate custom OpenAPI schema with detailed documentation"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Sales Research API",
        version="1.0.0",
        description="""
        # Sales Research API Documentation

        ## Overview
        The Sales Research API provides automated company research capabilities powered by AI. 
        It analyzes company websites and enriches the data with additional information to 
        provide comprehensive sales intelligence.

        ## Authentication
        All endpoints require API key authentication via the `X-API-Key` header.
        ```
        X-API-Key: your-api-key
        ```

        ## Rate Limiting
        - Basic tier: 100 requests/hour
        - Professional tier: 1000 requests/hour
        - Enterprise tier: Custom limits

        ## Error Handling
        The API uses standard HTTP status codes:
        - 200: Success
        - 400: Invalid request
        - 401: Authentication error
        - 429: Rate limit exceeded
        - 500: Server error

        Each error response includes:
        ```json
        {
            "detail": "Error description",
            "error_code": "ERROR_CODE",
            "timestamp": "2024-12-13T12:00:00Z"
        }
        ```

        ## Caching
        Research results are cached for 24 hours by default. Use `force_refresh=true` to bypass cache.
        """,
        routes=app.routes,
    )

    # Security Schemes
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }

    # Example Requests and Responses
    openapi_schema["paths"]["/api/v1/research"]["post"]["requestBody"] = {
        "content": {
            "application/json": {
                "examples": {
                    "basic_research": {
                        "summary": "Basic Research Request",
                        "value": {
                            "company_url": "https://example.com",
                            "depth": "basic",
                            "focus_areas": ["tech_stack", "decision_makers"],
                            "output_format": "json"
                        }
                    },
                    "deep_research": {
                        "summary": "Deep Research Request",
                        "value": {
                            "company_url": "https://example.com",
                            "depth": "deep",
                            "focus_areas": [
                                "tech_stack",
                                "decision_makers",
                                "market_position",
                                "competitors"
                            ],
                            "output_format": "markdown",
                            "force_refresh": True
                        }
                    }
                }
            }
        }
    }

    # Add response examples
    research_responses = {
        "200": {
            "description": "Successful research initiation",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Research Job Created",
                            "value": {
                                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                                "status": "pending",
                                "eta_seconds": 30
                            }
                        }
                    }
                }
            }
        },
        "4XX": {
            "description": "Client error",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_url": {
                            "summary": "Invalid URL",
                            "value": {
                                "detail": "Invalid company URL provided",
                                "error_code": "INVALID_URL",
                                "timestamp": "2024-12-13T12:00:00Z"
                            }
                        },
                        "rate_limit": {
                            "summary": "Rate Limit Exceeded",
                            "value": {
                                "detail": "Rate limit exceeded. Please try again later.",
                                "error_code": "RATE_LIMIT_EXCEEDED",
                                "timestamp": "2024-12-13T12:00:00Z"
                            }
                        }
                    }
                }
            }
        }
    }

    openapi_schema["paths"]["/api/v1/research"]["post"]["responses"] = research_responses

    # Add detailed parameter descriptions
    research_parameters = {
        "company_url": {
            "description": "The website URL of the company to research",
            "example": "https://example.com"
        },
        "depth": {
            "description": """
            Research depth level:
            - basic: Quick analysis of main pages
            - deep: Comprehensive analysis including subpages
            """,
            "enum": ["basic", "deep"],
            "default": "basic"
        },
        "focus_areas": {
            "description": """
            Specific areas to focus the research on:
            - tech_stack: Technology stack and infrastructure
            - decision_makers: Key executives and decision makers
            - market_position: Industry standing and competitive analysis
            - products: Product and service offerings
            - competitors: Competitor analysis and market comparison
            - funding: Investment and financial status
            """,
            "items": {
                "type": "string",
                "enum": [
                    "tech_stack",
                    "decision_makers",
                    "market_position",
                    "products",
                    "competitors",
                    "funding"
                ]
            },
            "default": []
        },
        "output_format": {
            "description": """
            Desired format of the research output:
            - json: Structured JSON format for programmatic processing
            - markdown: Formatted markdown text for human reading
            """,
            "enum": ["json", "markdown"],
            "default": "json"
        },
        "force_refresh": {
            "description": "Force new research instead of using cached data",
            "type": "boolean",
            "default": False
        }
    }

    # Add parameter descriptions to schema
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if "parameters" in operation:
                for param in operation["parameters"]:
                    if param["name"] in research_parameters:
                        param.update(research_parameters[param["name"]])

    # Add detailed response schemas
    openapi_schema["components"]["schemas"]["ResearchJobStatus"] = {
        "type": "object",
        "properties": {
            "job_id": {
                "type": "string",
                "format": "uuid",
                "description": "Unique identifier for the research job"
            },
            "status": {
                "type": "string",
                "enum": [
                    "pending",
                    "crawling",
                    "analyzing",
                    "enriching",
                    "synthesizing",
                    "completed",
                    "failed"
                ],
                "description": "Current status of the research job"
            },
            "progress": {
                "type": "number",
                "format": "float",
                "minimum": 0,
                "maximum": 1,
                "description": "Progress percentage (0.0 to 1.0)"
            },
            "created_at": {
                "type": "string",
                "format": "date-time",
                "description": "Timestamp when the job was created"
            },
            "updated_at": {
                "type": "string",
                "format": "date-time",
                "description": "Timestamp of the last status update"
            },
            "error": {
                "type": "string",
                "nullable": true,
                "description": "Error message if the job failed"
            }
        }
    }

    # Add example research results
    openapi_schema["components"]["examples"] = {
        "ResearchResult": {
            "value": {
                "company_intel": {
                    "company_name": "Example Corp",
                    "industry": "Technology",
                    "company_size": "1000-5000 employees",
                    "headquarters": "San Francisco, CA",
                    "founded_year": 2010,
                    "key_products": [
                        {
                            "name": "ExampleAPI",
                            "description": "Cloud-based API platform",
                            "target_market": "Enterprise developers"
                        }
                    ],
                    "key_executives": [
                        {
                            "name": "Jane Smith",
                            "title": "Chief Executive Officer",
                            "linkedin_url": "https://linkedin.com/in/janesmith"
                        }
                    ],
                    "technologies_used": [
                        "Python",
                        "Kubernetes",
                        "AWS",
                        "React"
                    ],
                    "competitive_advantages": [
                        "Market leader in API management",
                        "Strong enterprise customer base",
                        "Advanced security features"
                    ],
                    "recent_developments": [
                        "Launched new AI-powered features",
                        "Expanded European presence",
                        "Strategic partnership with Microsoft"
                    ]
                },
                "metadata": {
                    "generated_at": "2024-12-13T12:00:00Z",
                    "confidence_score": 0.85,
                    "data_freshness": "real-time",
                    "sources": [
                        "Company website",
                        "News articles",
                        "Social media"
                    ]
                }
            }
        }
    }

    # Add webhook documentation
    openapi_schema["paths"]["/api/v1/webhooks"] = {
        "post": {
            "summary": "Register webhook for job updates",
            "description": """
            Register a webhook URL to receive updates about research job status changes.
            The webhook will receive POST requests with the job status payload.
            """,
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "format": "uri",
                                    "description": "Webhook URL"
                                },
                                "events": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": [
                                            "job.completed",
                                            "job.failed",
                                            "job.status_changed"
                                        ]
                                    },
                                    "description": "Events to subscribe to"
                                }
                            }
                        },
                        "example": {
                            "url": "https://api.example.com/webhooks/research",
                            "events": ["job.completed", "job.failed"]
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Webhook registered successfully",
                    "content": {
                        "application/json": {
                            "example": {
                                "webhook_id": "wh_123456",
                                "status": "active"
                            }
                        }
                    }
                }
            }
        }
    }

    return openapi_schema

# app/api/docs/examples.py
"""Example requests and responses for documentation"""

EXAMPLE_REQUESTS = {
    "basic_research": {
        "company_url": "https://example.com",
        "depth": "basic",
        "focus_areas": ["tech_stack", "decision_makers"],
        "output_format": "json"
    },
    "deep_research": {
        "company_url": "https://example.com",
        "depth": "deep",
        "focus_areas": [
            "tech_stack",
            "decision_makers",
            "market_position",
            "competitors"
        ],
        "output_format": "markdown",
        "force_refresh": True
    }
}

EXAMPLE_RESPONSES = {
    "job_created": {
        "job_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "pending",
        "eta_seconds": 30
    },
    "job_status": {
        "job_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "analyzing",
        "progress": 0.45,
        "created_at": "2024-12-13T12:00:00Z",
        "updated_at": "2024-12-13T12:01:30Z"
    },
    "research_result": {
        "company_intel": {
            "company_name": "Example Corp",
            "industry": "Technology",
            "company_size": "1000-5000 employees",
            "headquarters": "San Francisco, CA",
            "founded_year": 2010,
            "key_products": [
                {
                    "name": "ExampleAPI",
                    "description": "Cloud-based API platform",
                    "target_market": "Enterprise developers"
                }
            ],
            "key_executives": [
                {
                    "name": "Jane Smith",
                    "title": "Chief Executive Officer",
                    "linkedin_url": "https://linkedin.com/in/janesmith"
                }
            ],
            "technologies_used": [
                "Python",
                "Kubernetes",
                "AWS",
                "React"
            ],
            "competitive_advantages": [
                "Market leader in API management",
                "Strong enterprise customer base",
                "Advanced security features"
            ],
            "recent_developments": [
                "Launched new AI-powered features",
                "Expanded European presence",
                "Strategic partnership with Microsoft"
            ]
        },
        "metadata": {
            "generated_at": "2024-12-13T12:00:00Z",
            "confidence_score": 0.85,
            "data_freshness": "real-time",
            "sources": [
                "Company website",
                "News articles",
                "Social media"
            ]
        }
    }
}

# Functions to integrate documentation with FastAPI app
def setup_docs(app):
    """Set up custom documentation for the FastAPI app"""
    app.openapi = lambda: custom_openapi(app)
    return app