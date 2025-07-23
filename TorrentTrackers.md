# Torrent trackers

Sometimes we need to share a big file, such as a large calculation. Uploading it to a cloud server can be very slow, the connection can be lost, the files can be corrupted, etc. In these cases, the ideal solution for Linux systems is [RSync](https://www.tecmint.com/rsync-local-remote-file-synchronization-commands/). An alternative option is to share our files by using a torrent download. This way, file sharing can be stopped and restarted without compromising the integrity of our data.  

Torrent trackers help people find each other. They don't store the files themselves, but they tell us who has them. When we create a new torrent, we just need to add the URL of some trackers to make sure our file is indexed properly.  

## Torrent clients

Install it to upload and download torrents.
- [Transmission](https://transmissionbt.com/) (easy to use)
- [qBittorrent](https://www.qbittorrent.org/) (more functions)

## Tracker lists

Updated lists with the best trackers available.
- [Newtrackon tracker list](https://newtrackon.com/)
- [Ngosang tracker list](https://ngosang.github.io/trackerslist/)
- [XIU2 tracker list](https://trackerslist.com/#/)
- [Torrends tracker list](https://torrends.to/torrent-tracker-list/)

## Tracker selection

Copy-and-paste selection of nice trackers (working on 2024-11):
```
udp://tracker.opentrackr.org:1337/announce

udp://tracker.torrent.eu.org:451

udp://opentracker.io:80/announce

udp://open.free-tracker.ga:6969/announce

udp://open.tracker.cl:1337/announce

udp://tracker.openbittorrent.com:6969/announce

udp://p2p.publictracker.xyz:6969/announce

http://tracker.openbittorrent.com:80/announce

http://tracker.bittorrent.am/announce
```

Some of these trackers are explained at:
- [opentrackr.org](https://opentrackr.org/) Used by Linux Mint
- [torrent.eu.org](https://torrent.eu.org/)
- [opentracker.io](https://opentracker.io/)
- [stealth.si](https://stealth.si/)

We can also use private trackers (without indexing, to share only with a friend etc). The problem is, these are not always reliable.
- [privtracker.com](https://privtracker.com/)
```
https://privtracker.com/RANDOMSTRING/announce
```

