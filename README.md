# CLI wrapper for the Clumio API

## Summary
A Python CLI wrapper for the Clumio API.

_Note: If you have any questions or comments you can always use GitHub discussions, or DM me on the twitter @rbocchinfuso._

#### Why
I have a customer using Veeam to perform VMware on-prem backups, and Clumio for off-prem (off-site) backups.  I needed a way to trigger backups with a post Veeam job completion script.  The idea being that the Veeam jobs run to local a local repository, once the job is complete the Clumio on-demand job is triggered by a post command.  This avoids the inevitable Veeam and Clumio VM snapshot conflict.

#### Todo
- Add any other relevant CLI commands.

## Requirements
- Python 3
	- [Anaconda](https://www.anaconda.com/products/individual) is a good choice, and what I use regardless of platform.
- All other requirements are in the _requirements.txt_ file.
```pip install -r requirements.txt```


## Usage
- Download code from GitHub
```
git clone https://github.com/rbocchinfuso/ClumioCLI.git
```
- Note:  If you don't have Git installed you can also just grab the zip: https://github.com/rbocchinfuso/ClumioCLI/archive/master.zip

- Copy config.ini.example to config.ini and modify as required

```
Python CLI wrapper for the Clumio API

Usage:
  clumio-cli.py getvcs
  clumio-cli.py getvms
  clumio-cli.py backup <group>
  clumio-cli.py groups
  clumio-cli.py config
  clumio-cli.py (-h | --help)
  clumio-cli.py --version

Options:
  -h --help             Show this screen.
  --version             Show version.
  
Commands:
  getvcs                Query Clumio API to get vCenter(s) ID
  getvms                Query and build VM List via Clumio API.
  backup <group>        Initiate Clumio on-demand backup for VMs in group.
  groups                List group KEY : VALUE (group : vm list) pairs.
  config                List all config KEY : VALUE pairs.
```
## Examples

### getvcs
```
(clumio) cabox@bocchi-dev01:~/workspace/clumio$ ./clumio-cli.py getvcs

+------+---------+---------------------------+--------------------------+-----------+-----------------+--------------------------------+
|   id | type    | ip_address                | endpoint                 | status    | backup_region   | cloud_connector_download_url   |
+======+=========+===========================+==========================+===========+=================+================================+
|   75 | on_prem | foo.bar.com               | foo.bar.com              | connected | us_east         | URL                            |    
+------+---------+---------------------------+--------------------------+-----------+-----------------+--------------------------------+
```

### getvms
![getvms](/assets/getvms.png)


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request ツ

## History
-  version 0.1.0 (initial release) - 2020/12/15

## Credits
Rich Bocchinfuso <<rbocchinfuso@gmail.com>>

## License
MIT License

Copyright (c) [2020] [Richard J. Bocchinfuso]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.