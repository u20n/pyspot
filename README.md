### Focuses
- Linux First
- \(near\) intended integration w/ spotify's api
- no non-standard dependencies
- as maintenace free as possible

### Configuration
Create either a JSON or XML file following the name standard of `*.cfg.<json/xml>`, e.g. `test.cfg.json`

**JSON**
```json
  {
    "c": {
      "id": <client_id(spotify)>,
      "secret": <client_secret(spotify)>
    }
  }
```
### TODO:

[ ] `/tmp` as dump from the [linux standard]( https://refspecs.linuxfoundation.org/FHS_2.3/fhs-2.3.html) - While not strictly nessecary, garbage collection in `/tmp` would be nice

[ ] pull current track; [API](https://developer.spotify.com/documentation/web-api/)

[ ] [XML](https://docs.python.org/3/library/xml.etree.elementtree.html) or [JSON](https://docs.python.org/3/library/json.html?highlight=json#module-json) formatting for track information

[ ] Optional cross-session rentention (e.g. `/var/tmp` instead of `/tmp`) 

[ ] Default 'icon' provided for example, but as hands off as possible
