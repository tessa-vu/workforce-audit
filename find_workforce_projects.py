"""
Disclaimers and Copyright

Copyright © 2026 Esri

All rights reserved under the copyright laws of the United States and applicable international laws, treaties, and conventions.
You may freely redistribute and use this sample code, with or without modification,
provided you include the original copyright notice and use restrictions.

Disclaimer: THE SAMPLE CODE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL ESRI OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Esri
Attn: Contracts and Legal Services Department
380 New York Street
Redlands, California, 92373-8100 USA
email: contracts@esri.com

Additional Disclaimers

    - This code snippet is not maintained and/or supported by Esri Technical Support or Staff
    - This code is not guaranteed for stability or accuracy 
    - Esri & its staff cannot be held liable for any direct or indirect damages incurred by running this code 
    - Use at Your Own Risk
    
Please make sure to thoroughly review this Code Sample and seek appropriate legal and technical advice before using it in any environment. 
You are encouraged to customize and adapt this Code Sample to meet your specific needs and requirements.
"""

"""
List every ArcGIS Workforce project (Classic and V2) in an ArcGIS Online organization.
"""

import argparse
import getpass

import pandas as pd
from arcgis.gis import GIS

# Portal search API query limits.
SEARCH_LIMIT = 10_000

COLUMNS = ["version", "title", "id", "owner", "access", "created", "modified", "url"]


# Not datetime, importing arcgis in ArcGIS Pro rebinds `datetime` in __main__ to module.
def _date(epoch_ms):
    return pd.Timestamp(epoch_ms, unit="ms").strftime("%Y-%m-%d")


def _search(gis, query):
    items = gis.content.search(query, max_items=SEARCH_LIMIT)
    if len(items) >= SEARCH_LIMIT:
        raise RuntimeError(
            f"Search hit the {SEARCH_LIMIT:,}-result cap, so results are incomplete: {query}"
        )
    return items


def _row(item, version):
    return {
        "version": version,
        "title": item.title,
        "id": item.id,
        "owner": item.owner,
        "access": item.access,
        "created": _date(item.created),
        "modified": _date(item.modified),
        "url": item.homepage,
    }


def find_workforce_projects(gis):
    """Return a DataFrame of Classic and V2 Workforce projects visible to the signed-in user."""
    # Portal search is fuzzy (re-check type and keyword exactly) as arcgis.apps.workforce does.
    classic = [
        item
        for item in _search(gis, 'type:"Workforce Project"')
        if item.type == "Workforce Project"
    ]
    v2 = [
        item
        for item in _search(
            gis, 'type:"Feature Service" AND typekeywords:"Workforce Project"'
        )
        if item.type == "Feature Service" and "Workforce Project" in item.typeKeywords
    ]
    rows = [_row(item, "Classic") for item in classic] + [
        _row(item, "V2") for item in v2
    ]
    return pd.DataFrame(rows, columns=COLUMNS).sort_values(
        ["owner", "title"], ignore_index=True
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        default="https://www.arcgis.com",
        help="Portal URL used with --username (default: %(default)s)",
    )
    parser.add_argument(
        "--username",
        help="Sign in as this built-in account (prompts for password). "
        "Omit to use the active ArcGIS Pro sign-in, which also covers SAML/enterprise logins.",
    )
    parser.add_argument(
        "--out",
        default="workforce_projects.csv",
        help="CSV output path (default: %(default)s)",
    )
    args = parser.parse_args()

    if args.username:
        gis = GIS(
            args.url, args.username, getpass.getpass(f"Password for {args.username}: ")
        )
    else:
        gis = GIS("pro")
    print(f"Signed into {gis.properties.name} as {gis.users.me.username}")

    projects = find_workforce_projects(gis)
    projects.to_csv(args.out, index=False)
    print(projects["version"].value_counts().to_string())
    print(f"{len(projects)} Workforce projects written to {args.out}")


if __name__ == "__main__":
    main()
