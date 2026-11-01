#!/usr/bin/env python3
"""Busca os números reais no GitHub e regenera assets/numeros.png."""
import os, json, subprocess, sys, urllib.request, datetime, pathlib

USER = os.environ.get("GH_USER", "Danielysouza")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def api(url, data=None):
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
        "User-Agent": "perfil-dani"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

# repositórios públicos e estrelas
repos, page = [], 1
while True:
    lote = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner")
    repos += lote
    if len(lote) < 100: break
    page += 1
estrelas = sum(r["stargazers_count"] for r in repos)

# commits no ano (últimos 12 meses)
agora = datetime.datetime.now(datetime.timezone.utc)
de = (agora - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
ate = agora.strftime("%Y-%m-%dT%H:%M:%SZ")
q = ('query{user(login:"%s"){contributionsCollection(from:"%s",to:"%s")'
     '{totalCommitContributions contributionCalendar{weeks{contributionDays{contributionCount}}}}}}') % (USER, de, ate)
res = api("https://api.github.com/graphql", json.dumps({"query": q}).encode())
col = res["data"]["user"]["contributionsCollection"]
commits = col["totalCommitContributions"]
semanas = [[d["contributionCount"] for d in w["contributionDays"]] for w in col["contributionCalendar"]["weeks"]]

numeros = [[str(len(repos)), "repositórios"], [str(estrelas), "estrelas"], [str(commits), "commits no ano"]]
print("Números:", numeros)

raiz = pathlib.Path(__file__).resolve().parent.parent
env = dict(os.environ, NUMEROS=json.dumps(numeros), CONTRIB=json.dumps(semanas))
subprocess.run([sys.executable, str(raiz / "gerar.py")], check=True, env=env)
