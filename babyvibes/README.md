# BabyVibes shop (WordPress + WooCommerce + Elementor)

An online shop for moms and babies. It launches with one product, the Talking Cactus, and is built to grow:
the homepage and shop list products automatically, so new products appear as soon as you publish them.
Everything is in one plugin, `dist/babyvibes-store-kit.zip`. Upload it, fill in three fields, and it builds the
shop.

## What the plugin sets up

- **Your first product, the Talking Cactus** (SKU `BV-TC-001`, category Toys), with description, short
  description, shipping weight and size. You add the photos.
- **Four pages built with Elementor**, editable as normal: Home, About, FAQ & Delivery, Contact. The Home page
  has these sections:
  - hero with a "Shop now" button
  - trust strip
  - **New arrivals** (your latest 8 products)
  - a **Spotlight** on the Talking Cactus
  - **Shop by category** (categories that have products)
  - **Best sellers**
  - FAQ
  - closing call to action
- **Homepage** set to the Home page, and a **main menu** (Home, Shop, About, FAQ & Delivery, Contact) placed
  in the theme's header.
- **South African store settings**: rand (ZAR), selling and delivering in South Africa only.
- **Normal store checkout**: "Add to cart" keeps shoppers browsing, and the cart, related products and shop
  page work as standard WooCommerce. A "Delivery across SA · Secure checkout · Help on WhatsApp" line shows
  under every product's buy button.
- **BabyVibes look**: Fredoka headings, Nunito text, green buttons, peach and cream backgrounds, rounded
  product cards, and styles for the shop, product pages, cart and checkout.

## Adding more products

1. Products > Add New: add a name, price, description, photos and an age guide.
2. Choose a **category** (create new ones such as Feeding, Bath time or Sleep on the right). Categories show
   up in "Shop by category" once they have a product.
3. Publish. The product appears in New arrivals, the shop and its category straight away.

Optional extras:

- Tick **Featured** (the ☆ in the Products list) to build a "Featured" section later.
- Change which product the homepage **Spotlight** features by editing that section in Elementor (heading, text
  and button link).
- While the shop has only one or two products, you may want to hide the "Best sellers" section (Elementor:
  right-click the section > Hide on desktop/tablet/mobile), since it will repeat New arrivals.

## Build it (about 20 minutes)

1. **Theme**: Appearance > Themes > Add New, install and activate **Hello Elementor**.
2. **Plugins**: Plugins > Add New, install and activate **Elementor** and **WooCommerce**. Skip or finish the
   WooCommerce setup wizard; the kit sets the store basics anyway.
3. **Upload the kit**: Plugins > Add New > Upload Plugin, choose `dist/babyvibes-store-kit.zip`, and activate.
4. **Run setup**: open the new **BabyVibes** menu in the admin, then enter:
   - the Talking Cactus price (for example 349)
   - your WhatsApp number (082 123 4567 works)
   - your shop email

   Then click **Set up my store**. Each step reports back with links.
5. **Add photos**: follow the link to the product and set the product image plus 3 to 5 gallery images
   (square, at least 1000 × 1000 px, light background). The homepage "Get yours" section shows them.
6. **Elementor site settings**: on any page, choose Edit with Elementor > ☰ > Site Settings:
   - Global Colors: Primary `#2F7A4D`, Secondary `#FF7F6E`, Text `#2E2A3B`, Accent `#FFD166`
   - Global Fonts: Primary and Secondary `Fredoka`, Text and Accent `Nunito`
   - Site Identity: upload your logo and site icon
   - Header & Footer (Hello theme): choose a header layout, then add the footer copyright and links
7. **Payments** (WooCommerce > Settings > Payments). For South Africa, install one of these and connect your
   merchant account: **PayFast**, **Yoco**, or **Ozow** (Instant EFT). Run one test order before going live.
8. **Delivery** (WooCommerce > Settings > Shipping): add a zone "South Africa" with a flat rate (for example
   R99) and optionally free delivery over an amount. For automatic courier rates, look at **The Courier Guy**
   or **Pudo** plugins.
9. **Legal pages**: Settings > Privacy creates a privacy policy (have it cover POPIA). Add a Terms page and link
   both, plus FAQ & Delivery, in the footer. The returns wording on the FAQ & Delivery page is a draft
   (7 days, refund within 5 working days). Make sure it matches what you actually offer and the Consumer
   Protection Act.

## Before you go live, check

- [ ] The product claims (repeats what you say, sings and dances, lights up, USB rechargeable, volume switch
      under the pot) match the cactus you're selling. Edit them on the product and on the Home page if they
      don't.
- [ ] The age rating from the packaging is in the product description and the FAQ. Listen to the songs on
      your stock: some talking cactus toys have shipped with unsuitable song lyrics.
- [ ] Delivery times on the FAQ & Delivery page and in the FAQ ("packed the same day before 12:00",
      "2 to 4 working days") are what you can deliver.
- [ ] Test order completed, and the order emails arrive (WooCommerce > Settings > Emails).
- [ ] The site looks right on your phone.
- [ ] Settings > Reading: "Discourage search engines" is unticked, once you move off the test subdomain.

## Editing later

Edit pages directly in Elementor. If you click "Run setup again", your pages are left alone unless you tick
**Rebuild the pages**, which replaces them with the original templates.

To change the templates themselves (for developers): edit `tools/build_templates.py` and run
`python3 tools/build_templates.py`. It regenerates `plugin/babyvibes-store-kit/templates/*.json` and the zip.
Each template JSON can also be imported on its own in Elementor (Templates > Saved Templates > Import).

The homepage illustration is `tools/cactus.svg`, embedded in the page (no upload needed). As the range grows,
swap the hero illustration for a banner photo of your products, and the Spotlight illustration for a photo of
whichever product you're featuring.

## Files

| Path | What it is |
|---|---|
| `dist/babyvibes-store-kit.zip` | The plugin to upload |
| `plugin/babyvibes-store-kit/` | Plugin source: setup screen (`includes/setup.php`), shop tweaks (`includes/store.php`), styles (`assets/store.css`), page templates (`templates/`) |
| `tools/build_templates.py` | Builds the Elementor page templates and the zip |
| `tools/cactus.svg` | Talking Cactus illustration used on the homepage |
