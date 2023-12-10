#!/bin/bash

# Install smimesign
echo "Installing smimesign..."
brew install smimesign

# Configure Git to use smimesign for signing
git config --global gpg.format x509
git config --global gpg.x509.program smimesign
git config --global gpg.x509.signingkey [Your-SMIME-Certificate-ID]

echo "smimesign setup complete."
