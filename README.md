# workforce-audit

### Disclaimers and Copyright

#### Copyright © 2026 Esri

#### All rights reserved under the copyright laws of the United States and applicable international laws, treaties, and conventions. You may freely redistribute and use this sample code, with or without modification, provided you include the original copyright notice and use restrictions.

#### Disclaimer: THE SAMPLE CODE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ESRI OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

##### Esri <p>Attn: Contracts and Legal Services Department</p><p>380 New York Street</p><p>Redlands, California, 92373-8100 USA</p><p>email: contracts@esri.com</p>


#### Additional Disclaimers

    - This code snippet is not maintained and/or supported by Esri Technical Support or Staff
    - This code is not guaranteed for stability or accuracy 
    - Esri & its staff cannot be held liable for any direct or indirect damages incurred by running this code 
    - Use at Your Own Risk
    
#### Please make sure to thoroughly review this Code Sample and seek appropriate legal and technical advice before using it in any environment. 
#### You are encouraged to customize and adapt this Code Sample to meet your specific needs and requirements.

---

Lists every [ArcGIS Workforce](https://support.esri.com/en-us/knowledge-base/deprecation-arcgis-workforce-000038426) project in an ArcGIS Online organization with its owner so admins can plan moving to Tasks in ArcGIS Field Maps.

- **Classic** Projects: Items of type `Workforce Project`.
- **V2** Projects: `Feature Service` items with typeKeyword `Workforce Project`.

**Run it as an org administrator.** Search returns only items the signed-in user can access.

## ArcGIS Online Notebook

Upload `find_workforce_projects.ipynb` to ArcGIS Online. Open with the Standard runtime and run all cells. The CSV is saved to `/arcgis/home/workforce_projects.csv`.

## Local (ArcGIS Pro Python)

```powershell
propy find_workforce_projects.py                       # uses active ArcGIS Pro sign-in
propy find_workforce_projects.py --username jdoe       # built-in account, prompts for password
propy find_workforce_projects.py --out C:\temp\wf.csv
```

Output Columns: `version`, `title`, `id`, `owner`, `access`, `created`, `modified`, `url`.

### `InsecureRequestWarning` Messages

You may see many `InsecureRequestWarning: Unverified HTTPS request` messages that come from a thread-safety bug in `truststore` 0.10.0 which is the version bundled with `arcgis` 2.4.3. `arcgis` runs searches on several threads at once and the bug can loosen certificate checks for a connection while that happens, so don't just hide the warning. However, the script's results are not affected.

The fix is `truststore` 0.10.5 or later, and `pyarrow` between 17.0.0 and 24.0.0. ArcGIS Pro's default environment (`arcgispro-py3`) can't be modified so clone it first then run this in the clone env:

```powershell
python -m pip install --upgrade "truststore>=0.10.5" "pyarrow>=17,<24"
```
