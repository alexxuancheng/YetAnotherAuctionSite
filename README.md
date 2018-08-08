# YetAnotherAuctionSite-YAAS

YAAS is a web application and a web service to create and participate in auctions. Examples of popular
auction​ ​sites​ ​include​ ​​ebay.com​​ ​and​ ​​huuto.net​.

Implemented Requirements:
1. Create an user account
• Any anonymous user can create a new regular user account;
• Django admin interface are enabled;
• Administrator user account are created via Django admin interface;
2. Edit account information
• authenticated user can change his/her email, and password;
3. UC3 Create a new auction
• Any registered user can create a new account;
• The created auction has the following information:
• Confirm by email
4. Edit the description of an auction
• The seller of an auction can change the description of the auction;
5. Browse and Search auctions
• Both anonymous and registered users can browse the list of the auctions and search auction by auction name;
6. Bid
• Any registered user can bid for an active auction, except the seller;
• minimum bid increment is 0.01;
• the seller can’t bid on his/her own auctions;
• show the most recent description of the auction before accepting any bids;
• a new bid should be greater than min price and any previous bids;
• the seller of the auction, new bidder, the previous bidders will notified by email that a new bid has beed registered;
• softdeadline
7. Ban an auction
• Anadministratorcanbananactiveauction;
• Thebannedauctionisnotdeletedfromthesystem,itwillnotshowonthe auction list or search result;
• Thebannedauctionwillnotberesolved;
• Thesellerandallthebiddersarenotifiedbyemailthattheauctionisbanned;
8. Resolve auction
• Afterthedeadlineoftheauction,thesystemautomaticallyresolvetheauction and elect the winner.
• Allbiddersandthesellerarenotifiedbyemailthattheauctionhasbeen resolved;
9. Support for multiple languages
10. Support multiple concurrent sessions 
11. Support for currency exchange
12. Browse and search via API
13. Bid via API
14. Database fixture
15. Automated functional tests
