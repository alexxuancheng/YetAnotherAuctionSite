# YetAnotherAuctionSite-YAAS

YAAS is a web application and a web service to create and participate in auctions. Examples of popular
auction​ ​sites​ ​include​ ​​ebay.com​​ ​and​ ​​huuto.net​.
An auction site is a good example of a service offered as a web application. The organization owning an auction site does not buy or sell anything. Instead, it creates a community of users interested in buying or selling the most diverse items and provides its members with the tools to communicate and interact in​ ​a​ ​convenient,​ ​fast​ ​and​ ​easy​ ​way.
In​ ​the​ ​rest​ ​of​ ​this​ ​section,​ ​we​ ​describe​ ​the​ ​main​ ​requirements​ ​for​ ​the​ ​YAAS​ ​web​ ​application​ ​and​ ​web service.
2. Implemented Requirements:
2.1. UC1 create an user account
• Any anonymous user can create a new regular user account;
• Django admin interface are enabled;
• Administrator user account are created via Django admin interface;
2.2 UC2 Edit account information
• authenticated user can change his/her email, and password;
2.3 UC3 Create a new auction
• Any registered user can create a new account;
• The created auction has the following information:
- seller: the user who created the auction;
- name: the name of the auction;
- description: description of the auction;
- minprice: starting price of the auction;
- deadline: the end date of the auction, minimum duration is 72 hours from the time the auction is created.
• Confirm by email: after create the auction, the seller(who create the auction) receive a
confirmation email. The seller must click the confirmation link in the email to activate the auction, otherwise the auction is inactivated and will not show on the auction list.
• OP1(optional features):
 - the confirmation email also include a link, which allow the user to see the created auction without login;
- auction has a life cycle: active, banned, due, adjudicated:
- when the auction is created, all these four features is False;
- active: after the user confirm the email, the active become True; the auction will keep
active until its deadline, or it is banned;
- banned: An administrator can ban the auction, the banned auction can’t be bid, and will
not show on the auction list.
- due: auction due is True after the deadline ends;
- adjudicated: after due turns True, the auction is adjudicated automatically by the
system, and a winner is selected;
2.4 UC4 Edit the description of an auction
• The seller of an auction can change the description of the auction;
2.5 UC5 Browse and Search auctions
• Both anonymous and registered users can browse the list of the auctions and search auction by auction name;
2.6 UC6 Bid
• Any registered user can bid for an active auction, except the seller;
• minimum bid increment is 0.01;
• the seller can’t bid on his/her own auctions;
• show the most recent description of the auction before accepting any bids;
• a new bid should be greater than min price and any previous bids;
• the seller of the auction, new bidder, the previous bidders will notified by email that a new bid has beed registered;
• OP2:
- softdeadline:ifabidismadewithinfiveminutesbeforethedeadline,theacution’s deadline will be extends automatically additional 5 minutes;
2.7 UC7 Ban an auction
• Anadministratorcanbananactiveauction;

• Thebannedauctionisnotdeletedfromthesystem,itwillnotshowonthe auction list or search result;
• Thebannedauctionwillnotberesolved;
• Thesellerandallthebiddersarenotifiedbyemailthattheauctionisbanned;
2.8 UC8 Resolve auction
• Afterthedeadlineoftheauction,thesystemautomaticallyresolvetheauction and elect the winner.
• Allbiddersandthesellerarenotifiedbyemailthattheauctionhasbeen resolved;
2.9 UC9 Support for multiple languages
2.10 UC10 Support multiple concurrent sessions 2.11 UC11 Support for currency exchange
2.12 WS1 Browse and search via API
2.13 WS2 Bid via API
2.14 TR1 Database fixture
2.15 TR2 Automated functional tests
