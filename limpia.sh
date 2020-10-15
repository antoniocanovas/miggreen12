git add .gitmodules
git rm --cached account-financial-tools
rm -r account-financial-tools
git rm --cached community-data-files
rm -r community-data-files
git rm --cached knowledge
rm -r knowledge
git rm --cached l10n-spain
rm -r l10n-spain
git rm --cached partner-contact
rm -r partner-contact
git rm --cached project
rm -r project
git rm --cached server-tools
rm -r server-tools
git rm --cached server-ux
rm -r server-ux
git rm --cached web
rm -r web
git rm --cached SerpentCS_Contributions
rm -r SerpentCS_Contributions
git add .
git status 
git commit -m "limpio"
git push

