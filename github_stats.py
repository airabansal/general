"""GitHub stats fetcher: show a user's profile stats and their top repos.

Uses GitHub's public REST API (no login needed for basic use). If you hit the
rate limit, set a personal access token in the GITHUB_TOKEN env var for a much
higher limit:  export GITHUB_TOKEN=your_token
"""

import os
from datetime import datetime, timedelta

import requests

API_BASE = "https://api.github.com"


def _headers():
    """Build request headers, adding auth only if a token is available."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_user(username):
    """Fetch a user's profile. Returns parsed JSON dict."""
    resp = requests.get(
        f"{API_BASE}/users/{username}", headers=_headers(), timeout=10
    )
    resp.raise_for_status()
    return resp.json()


def get_top_repos(username, count=5):
    """Fetch the user's repos and return the top `count` by star count."""
    repos = []
    # GitHub paginates at 100 per page; grab up to 100 for a simple project.
    resp = requests.get(
        f"{API_BASE}/users/{username}/repos",
        headers=_headers(),
        params={"per_page": 100, "type": "owner"},
        timeout=10,
    )
    resp.raise_for_status()
    repos = resp.json()
    repos.sort(key=lambda r: r["stargazers_count"], reverse=True)
    return repos[:count]


def get_commit_count_last_6_months(username):
    """Return the count of public commits authored by the user in ~6 months.

    Uses the Search Commits API, which needs a token and counts only public
    commits attributed to the user's identity. Returns an int, or raises.
    """
    since = (datetime.utcnow() - timedelta(days=182)).strftime("%Y-%m-%d")
    query = f"author:{username} committer-date:>={since}"
    resp = requests.get(
        f"{API_BASE}/search/commits",
        headers=_headers(),
        params={"q": query, "per_page": 1},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["total_count"]


def show_user(user, top_repos, commit_count=None):
    """Print a friendly summary of the profile and top repos."""
    print(f"\n{user.get('name') or user['login']}  (@{user['login']})")
    if user.get("bio"):
        print(f"  {user['bio']}")
    if user.get("location"):
        print(f"  Location  : {user['location']}")
    print(f"  Repos     : {user['public_repos']}")
    print(f"  Followers : {user['followers']}   Following: {user['following']}")
    print(f"  Joined    : {user['created_at'][:10]}")
    if commit_count is not None:
        print(f"  Commits   : {commit_count} (public, last 6 months)")
    print(f"  Profile   : {user['html_url']}")

    if top_repos:
        print("\n  Top repositories by stars:")
        for repo in top_repos:
            stars = repo["stargazers_count"]
            lang = repo.get("language") or "-"
            print(f"    ★ {stars:<6} {repo['name']}  ({lang})")
    print()


def main():
    username = input("Enter a GitHub username: ").strip()
    if not username:
        print("No username entered.")
        return

    try:
        user = get_user(username)
        top_repos = get_top_repos(username)
    except requests.exceptions.HTTPError as err:
        status = err.response.status_code
        if status == 404:
            print(f"User '{username}' not found. Check the spelling.")
        elif status == 403:
            print(
                "Rate limit hit (HTTP 403). Wait a bit, or set a token: "
                "export GITHUB_TOKEN=your_token"
            )
        else:
            print(f"HTTP {status} error from GitHub.")
        return
    except requests.exceptions.RequestException as err:
        print(f"Network error: {err}")
        return

    # Commit count is best-effort: it needs a token and only covers public
    # commits, so a failure here should not sink the rest of the output.
    commit_count = None
    try:
        commit_count = get_commit_count_last_6_months(username)
    except requests.exceptions.RequestException:
        if not os.environ.get("GITHUB_TOKEN"):
            print("(Commit count skipped: set GITHUB_TOKEN to enable it.)")
        else:
            print("(Commit count unavailable right now.)")

    show_user(user, top_repos, commit_count)


if __name__ == "__main__":
    main()
