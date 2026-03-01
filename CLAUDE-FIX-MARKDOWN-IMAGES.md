# Fix Markdown Images (Obsidian → VSCode compatible)

## The Problem

Obsidian uses wikilink syntax for images and resolves them **vault-wide** (no path needed):

```
![[Pasted image 20260228190155.png]]
```

VSCode needs **standard CommonMark markdown** with a **relative path** from the markdown file to the image. It cannot resolve vault-wide image names.

Additionally, Obsidian dumps pasted images into a global attachments folder (often the vault root), not next to the markdown file that references them.

---

## The Fix (two steps)

### Step 1 — Move images next to their markdown file

Find which markdown file references each image, then move the image into the **same directory** as that file.

```bash
# find all markdown files that reference pasted images
grep -r "Pasted image" /path/to/vault --include="*.md" -l

# move images
mv "Pasted image TIMESTAMP.png" path/to/markdown-dir/descriptive-name.png
```

Tips:
- Rename images to descriptive, hyphen-separated names at this step (e.g. `msfvenom-payload.png`). No spaces in filenames — they cause problems in standard markdown links.
- If an image is unreferenced (orphan), decide whether to delete it or leave it in place.

### Step 2 — Update markdown references

Change `![[Pasted image TIMESTAMP.png]]` to standard markdown using the new filename:

```
![](descriptive-name.png)
```

**If you can't rename the file** and it has spaces in the name, use CommonMark angle-bracket syntax (works in both VSCode and Obsidian):

```
![](<Pasted image TIMESTAMP.png>)
```

Do **not** use `%20` URL encoding — it works but is ugly and hard to read.

---

## Obsidian Settings (prevent future issues)

In Obsidian → Settings → Files and Links:

- **Default location for new attachments** → set to `Same folder as current file`
- **New link format** → set to `Relative path to file`
- **Use [[Wikilinks]]** → turn **off** (use standard markdown links instead)

With these settings, Obsidian will paste images next to the current note and use `![](image.png)` syntax that VSCode also understands.

---

## Quick Reference

| Syntax | Obsidian | VSCode |
|---|---|---|
| `![[image.png]]` | ✅ | ❌ |
| `![](image.png)` | ✅ | ✅ (image must be in same dir) |
| `![](<image with spaces.png>)` | ✅ | ✅ (image must be in same dir) |
| `![](./subdir/image.png)` | ✅ | ✅ |
