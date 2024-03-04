{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs {
            inherit system;
          };
          nativeBuildInputs = with pkgs; [ pkg-config ];
          buildInputs = with pkgs; [
            poetry
            python310Packages.flake8
            python310Packages.isort
            python310Packages.mypy
            python310Packages.django-stubs
            python310Packages.django-environ
            python310Packages.pymysql
            python310Packages.whitenoise
            python310Packages.djangorestframework
            libargon2
            nodejs_21
          ];
        in
        with pkgs;
        {
          devShells.default = mkShell {
            inherit nativeBuildInputs buildInputs;
          };
        }
      );
}
