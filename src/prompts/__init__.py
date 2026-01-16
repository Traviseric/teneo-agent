"""
Teneo Agent Prompts
===================

Modular prompts for worker instructions.

Available prompts:
- create_worker_prompt: Main worker task prompt
- create_setup_prompt: Project setup prompt
"""

from .worker_prompts import create_worker_prompt, create_setup_prompt

__all__ = ["create_worker_prompt", "create_setup_prompt"]
