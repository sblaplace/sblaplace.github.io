{
  description = "Python dev env with pandas, matplotlib, numpy";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        # Pick a specific Python version exposed by your nixpkgs
        python = pkgs.python313;

        pythonEnv = python.withPackages (ps: with ps; [
          pandas
          matplotlib
          numpy
          ipython      # optional, but nice
        ]);
      in {
        devShells.default = pkgs.mkShell {
          name = "python-dev";
          buildInputs = [
            pythonEnv
          ];
        };
      }
    );
}

