# Zotero

Zotero is a free & open source reference manager. With just a few tweaks, it is the perfect tool to help you organize all your messy pdfs.

## Installing

First [download](https://www.zotero.org/download/) __Zotero for desktop__, and the browser addon __Zotero Connector__. If you are on Linux, it is best to download the Flatpak desktop install from [Flathub](https://flathub.org/apps/org.zotero.Zotero).  

The browser addon [Zotero Connector](https://www.zotero.org/download/) will automatically save the references from your browser with the click of a button: for example, if you are on the official webpage of a paper, it will automatically save all the related information, authors, DOI, etc.  

You definitely should also install the following plugins:
- [Better BibTex for Zotero](https://retorque.re/zotero-better-bibtex/installation/index.html), which lets you customize the citation keys
- [ZotMoov](https://github.com/wileyyugioh/zotmoov) to automatically rename the PDFs and save them on a custom folder, which you can sync with the cloud or else. ZotMoov works for all Zotero Versions. Note that ZotMoov is a replacement for [ZotFile](http://zotfile.com/#how-to-install--set-up-zotfile), an older and discontinued plugin which only works for Zotero versions lower than 7.
Another cool and useful plugin is:
- [Inciteful Zotero Plugin](https://github.com/inciteful-xyz/inciteful-zotero-plugin), which helps you find related literature.  

Finally, there is a native dark mode for the Linux Flatpak installation. But if you are on Windows and want a dark mode for Zotero, take a look at [Zotero Shadow](https://github.com/pablogila/ZoteroShadow).  

Some of these addons require a small configuration to work flawlessly, which is indicated below.  

## Automatic and custom citation keys

You can edit the automatic citation keys by going to `Settings, Better BibTex, Citation keys`. There you can modify the citation key formula, for example as `auth.lower + year` to have automatic citation keys such as _druzbicki2023_.  

You can also create a custom citation key for any particular reference, by editing the `Extra` section of said reference with `citation key: MyCustomKey`.  

## Renaming rules

Zotero 7 has new and easier [renaming rules](https://www.zotero.org/support/file_renaming). For example, you can rename your PDFs as:  
`\{{ citationKey }} - \{{ title }}`  

Zotero 6 had different rules, and also using ZotFile had a problem with subinexes; to fix those, check the [appendix](#renaming-titles-with-subindexes-via-zotfile). If you are using ZotMoov on Zotero v7 you can skip it.  

## Saving files to a custom folder

You can automatically save your pdfs to a custom folder (to sync it, etc) with ZotMoov.
Go to the Zotero 7 settings, to `Settings, Advanced, Files and Folders, Linked Attachment Base Directory`, and choose there your custom folder to save all tour PDFs.
Now, you must set the same folder in ZotMoov. To do that, go to `Settings, ZotMoov` and write the same folder on `Directory to Move Files To`. Also in ZotMoov settings, leave empty the `Source folder for Attaching New Files` setting. On ZotMoov's `Other Settings`, set `File Behavior` to `More`, and check all checkboxes.  

If you are using a Zotero version < 7, you can still use ZotMoov, or ZotFile instead (although it is discontinued). To automatically move your PDFs with ZotFile to a custom folder, go to `Tools, ZotFile Preferences, General Settings, Location of Files, Custom Location` and select your desired folder. This same folder should also be specified for Zotero itself, at `Edit, Preferences, Advanced, Files and Folders, Linked Attachment Base Directory`.  

## Supporting Information PDFs

It is recommended to save the Supporting Information (SI) of the papers by creating a copy of the corresponding reference (with a right click), adding `_Supplementary` at the end of the title, then attaching the supplementary pdf, and finally editing the citation key as `CitationKey_SI`. This prevents SI to be renamed incorrectly, since __ZotFile and ZotMoov only seems to work fine with one attachment per reference__.  

## Appendix

### Renaming titles with subindexes via ZotFile

For Zotero < v.7 with ZotFile.  
Some papers have subindexes on the title, such as in MAPbI<sub>3</sub>. These subindexes are rendered in HTML, using the tags `MAPbI<sub>3</sub>`. This is useful when referencing, but instead of saving titles as `MAPbI3`, ZotFile will incorrectly introduce those "sub" tags on the renamed PDFs by default. To remove HTML tags such as `<sub>` from the renamed pdf files, you need to configure a custom ZotFile User Wildcard. [(source)](https://github.com/jlegewie/zotfile/issues/455)  
To fix that, simply go to `Edit, Preferences, Advanced, Config Editor` and click on accept the risk (because if we are brave enough there is no risk). Search for `zotfile.wildcards.user`, and introduce the following text:  
```
{"1": {"field": "title", "operations":[{"function": "replace", "regex": "<sub>", "replacement":"", "flags":"g"},{"function": "replace", "regex": "</sub>", "replacement":"", "flags":"g"}]}}
```
You have now configured a custom User Wildcard. You can now extract the title without the HTML tags by writting `{\%1}` (without the `\`, it is needed for the stupid GitHub pages to work).  
on the ZotFile renaming rules, located in `Tools, ZotFile Preferences, Renaming Rules`.  
For example, to rename all PDFs as `CitationKey - Title`, you should configure ZotFile renaming rules as `{\%b} - {\%1}` (again without the `\`).  

