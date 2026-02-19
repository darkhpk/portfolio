#!/usr/bin/env python
"""
Generate a new SECRET_KEY for Django production use.
Run this script and copy the output to your .env file.
"""

from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("Generated Django SECRET_KEY:")
    print("="*70)
    print(f"\nSECRET_KEY={secret_key}")
    print("\n" + "="*70)
    print("Copy the line above to your .env file")
    print("="*70 + "\n")
