# pes-packages

A repository containing PKGBUILD scripts for the packages used to create PES.

## Package Signing

If you have an existing GPG key, import it:

```
gpg --import /path/to/private-key
```

Now edit the key and trust it:

```
$ gpg --edit KEY
gpg> trust 5
```

This key can now be used for signing packages.

## Building Packages

You can use the `buildpkg.sh` script to build an individual package and to add it to a pacman repository under `./repo`. E.g.

```bash
./buildpkg.sh pes-libcec
```

If you want to sit back and build **all** packages then run:

```bash
./makepkgs.sh
```

## Building pes-gui

If you already have a `pes.db` file which was built previously by the `pes-gui` package you can significantly reduce the build time of this package by re-using the `pes.db` file:

```bash
cd packages/pes-gui
makepkg -C -o
cp ~/git/pes-gui/src/pes/data/pes.db src/pes-gui/src/pes/data/
makepkg --sign --key $KEY
```

Here we remove any files from a previous build and just download the source for the package. Next we copy our `pes.db` file into the `src` directory and then finally, we build the package.
