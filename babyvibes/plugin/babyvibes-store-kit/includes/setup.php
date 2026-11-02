<?php
/**
 * Admin: one-click setup of the BabyVibes shop.
 *
 * Creates (or updates) the Talking Cactus product, the Home, About, FAQ & Delivery and Contact
 * pages from the bundled Elementor templates, the main menu, and sets the homepage and
 * South African store settings. Safe to run again: it updates what it created before.
 */

defined( 'ABSPATH' ) || exit;

const BABYVIBES_PAGES = array(
	'home'         => array( 'title' => 'Home', 'slug' => 'home' ),
	'about'        => array( 'title' => 'About', 'slug' => 'about' ),
	'faq-delivery' => array( 'title' => 'FAQ & Delivery', 'slug' => 'faq-delivery' ),
	'contact'      => array( 'title' => 'Contact', 'slug' => 'contact' ),
);

// Placeholders in the bundled templates, replaced with the details entered on the setup screen.
const BABYVIBES_PLACEHOLDER_WHATSAPP = '27000000000';
const BABYVIBES_PLACEHOLDER_EMAIL    = 'hello@babyvibes.co.za';

add_action(
	'admin_menu',
	function () {
		add_menu_page(
			__( 'BabyVibes', 'babyvibes' ),
			__( 'BabyVibes', 'babyvibes' ),
			'manage_options',
			'babyvibes-setup',
			'babyvibes_setup_screen',
			'dashicons-heart',
			56
		);
	}
);

function babyvibes_setup_defaults() {
	return wp_parse_args(
		get_option( 'babyvibes_setup', array() ),
		array(
			'price'    => '',
			'whatsapp' => '',
			'email'    => get_option( 'admin_email' ),
			'pages'    => array(),
		)
	);
}

function babyvibes_setup_screen() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$opts    = babyvibes_setup_defaults();
	$report  = null;
	$missing = array();
	if ( ! class_exists( 'WooCommerce' ) ) {
		$missing[] = 'WooCommerce';
	}
	if ( ! did_action( 'elementor/loaded' ) ) {
		$missing[] = 'Elementor';
	}

	if ( isset( $_POST['babyvibes_run'] ) && check_admin_referer( 'babyvibes_setup' ) ) {
		$opts['price']    = wc_format_decimal( wp_unslash( $_POST['price'] ?? '' ) );
		$opts['whatsapp'] = preg_replace( '/\D+/', '', wp_unslash( $_POST['whatsapp'] ?? '' ) );
		if ( 0 === strpos( $opts['whatsapp'], '0' ) ) {
			$opts['whatsapp'] = '27' . substr( $opts['whatsapp'], 1 ); // 082... -> 2782...
		}
		$opts['email'] = sanitize_email( wp_unslash( $_POST['email'] ?? '' ) );
		update_option( 'babyvibes_setup', $opts, false );

		if ( $missing ) {
			$report = array( array( 'error', 'Install and activate ' . implode( ' and ', $missing ) . ' first.' ) );
		} elseif ( '' === $opts['price'] || ! $opts['whatsapp'] || ! is_email( $opts['email'] ) ) {
			$report = array( array( 'error', 'Please fill in the price, WhatsApp number and email.' ) );
		} else {
			$report = babyvibes_run_setup( $opts, ! empty( $_POST['overwrite'] ) );
		}
	}
	?>
	<div class="wrap">
		<h1>BabyVibes: set up store</h1>
		<p>This creates the Talking Cactus product, the Home, About, FAQ &amp; Delivery and Contact pages (built with Elementor), the main menu, and sets your homepage and South African store settings. You can run it again at any time.</p>

		<?php if ( $missing && ! $report ) : ?>
			<div class="notice notice-warning"><p>Install and activate <strong><?php echo esc_html( implode( ' and ', $missing ) ); ?></strong> before running the setup (Plugins &gt; Add New).</p></div>
		<?php endif; ?>

		<?php if ( $report ) : ?>
			<div class="notice notice-<?php echo esc_attr( 'error' === $report[0][0] ? 'error' : 'success' ); ?>">
				<ul>
				<?php foreach ( $report as $line ) : ?>
					<li><?php echo wp_kses( $line[1], array( 'a' => array( 'href' => array(), 'target' => array() ), 'strong' => array() ) ); ?></li>
				<?php endforeach; ?>
				</ul>
			</div>
		<?php endif; ?>

		<form method="post">
			<?php wp_nonce_field( 'babyvibes_setup' ); ?>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><label for="bv-price">Talking Cactus price (R)</label></th>
					<td><input id="bv-price" name="price" type="text" inputmode="decimal" class="small-text" value="<?php echo esc_attr( $opts['price'] ); ?>" required> <span class="description">For example 349</span></td>
				</tr>
				<tr>
					<th scope="row"><label for="bv-wa">WhatsApp number</label></th>
					<td><input id="bv-wa" name="whatsapp" type="tel" class="regular-text" value="<?php echo esc_attr( $opts['whatsapp'] ); ?>" required> <span class="description">For example 082 123 4567</span></td>
				</tr>
				<tr>
					<th scope="row"><label for="bv-email">Shop email</label></th>
					<td><input id="bv-email" name="email" type="email" class="regular-text" value="<?php echo esc_attr( $opts['email'] ); ?>" required></td>
				</tr>
				<?php if ( ! empty( $opts['pages'] ) ) : ?>
				<tr>
					<th scope="row">Pages</th>
					<td><label><input name="overwrite" type="checkbox" value="1"> Rebuild the pages from the templates. <strong>This replaces any Elementor changes you made to them.</strong></label></td>
				</tr>
				<?php endif; ?>
			</table>
			<?php submit_button( empty( $opts['pages'] ) ? 'Set up my store' : 'Run setup again', 'primary', 'babyvibes_run' ); ?>
		</form>
	</div>
	<?php
}

/**
 * @return array List of [status, message] lines.
 */
function babyvibes_run_setup( array $opts, $overwrite ) {
	$log = array();

	// Store settings for South Africa.
	update_option( 'woocommerce_currency', 'ZAR' );
	update_option( 'woocommerce_currency_pos', 'left' );
	update_option( 'woocommerce_price_thousand_sep', ' ' );
	update_option( 'woocommerce_price_decimal_sep', '.' );
	update_option( 'woocommerce_price_num_decimals', '2' );
	if ( 0 !== strpos( (string) get_option( 'woocommerce_default_country' ), 'ZA' ) ) {
		update_option( 'woocommerce_default_country', 'ZA:GP' );
	}
	update_option( 'woocommerce_allowed_countries', 'specific' );
	update_option( 'woocommerce_specific_allowed_countries', array( 'ZA' ) );
	update_option( 'woocommerce_ship_to_countries', '' );
	// Non-AJAX add to cart, so "Buy now" can go straight to checkout.
	update_option( 'woocommerce_enable_ajax_add_to_cart', 'no' );
	update_option( 'woocommerce_cart_redirect_after_add', 'yes' );
	$log[] = array( 'ok', 'Store set to South Africa and rand (ZAR).' );

	// Product.
	$product_id = babyvibes_upsert_product( $opts['price'] );
	$log[]      = array( 'ok', sprintf( 'Talking Cactus product ready at R%s. <a href="%s">Add its photos</a> (main image and gallery).', esc_html( $opts['price'] ), esc_url( get_edit_post_link( $product_id, 'raw' ) ) ) );

	// Pages.
	$pages = $opts['pages'];
	foreach ( BABYVIBES_PAGES as $key => $page ) {
		$existing = isset( $pages[ $key ] ) ? get_post( $pages[ $key ] ) : null;
		if ( $existing && 'trash' !== $existing->post_status && ! $overwrite ) {
			$log[] = array( 'ok', sprintf( '%s page kept as it is.', esc_html( $page['title'] ) ) );
			continue;
		}
		$result = babyvibes_build_page( $key, $page, $existing ? $existing->ID : 0, $opts );
		if ( is_wp_error( $result ) ) {
			$log[] = array( 'error', esc_html( $page['title'] . ': ' . $result->get_error_message() ) );
			continue;
		}
		$pages[ $key ] = $result;
		$log[]         = array( 'ok', sprintf( '%s page built. <a href="%s" target="_blank">View</a>', esc_html( $page['title'] ), esc_url( get_permalink( $result ) ) ) );
	}
	$opts['pages'] = $pages;
	update_option( 'babyvibes_setup', $opts, false );

	// Homepage.
	if ( ! empty( $pages['home'] ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', (int) $pages['home'] );
		$log[] = array( 'ok', 'Home page set as the front page.' );
	}

	// Menu.
	babyvibes_build_menu( $pages );
	$log[] = array( 'ok', 'Main menu created (Appearance &gt; Menus).' );

	if ( class_exists( '\Elementor\Plugin' ) ) {
		\Elementor\Plugin::$instance->files_manager->clear_cache();
	}
	$log[] = array( 'ok', '<strong>Done.</strong> <a href="' . esc_url( home_url( '/' ) ) . '" target="_blank">Open your site</a>.' );
	return $log;
}

function babyvibes_upsert_product( $price ) {
	$id      = wc_get_product_id_by_sku( BABYVIBES_SKU );
	$product = $id ? wc_get_product( $id ) : new WC_Product_Simple();

	if ( ! $id ) {
		$product->set_name( 'Talking Cactus' );
		$product->set_slug( 'talking-cactus' );
		$product->set_sku( BABYVIBES_SKU );
		$product->set_short_description(
			'<p>The cheeky little cactus that repeats what you say, dances, sings and lights up. Giggles guaranteed.</p>'
		);
		$product->set_description( babyvibes_product_description() );
		$product->set_manage_stock( false );
		$product->set_stock_status( 'instock' );
		$product->set_catalog_visibility( 'visible' );
		$product->set_reviews_allowed( true );
		$product->set_weight( '0.4' );
		$product->set_length( '15' );
		$product->set_width( '15' );
		$product->set_height( '35' );
		$cat = term_exists( 'Toys', 'product_cat' );
		if ( ! $cat ) {
			$cat = wp_insert_term( 'Toys', 'product_cat' );
		}
		if ( ! is_wp_error( $cat ) ) {
			$product->set_category_ids( array( (int) $cat['term_id'] ) );
		}
	}
	$product->set_regular_price( $price );
	$product->set_status( 'publish' );
	return $product->save();
}

function babyvibes_product_description() {
	return implode(
		"\n",
		array(
			'<h3>Say hello to your little one\'s new favourite friend</h3>',
			'<p>Say something and the Talking Cactus says it right back in a giggly voice, then wiggles and dances. Switch to music mode for a playlist of catchy songs with flashing lights. It\'s soft, cheeky and impossible not to smile at.</p>',
			'<h4>What it does</h4>',
			'<ul>',
			'<li>Repeats what you say in a funny voice</li>',
			'<li>Sings and dances</li>',
			'<li>Colourful lights</li>',
			'<li>USB rechargeable, so no batteries to buy</li>',
			'</ul>',
			'<h4>In the box</h4>',
			'<ul><li>1 x Talking Cactus</li><li>1 x USB charging cable</li></ul>',
			'<h4>Safety</h4>',
			'<p>Please check the age rating on the packaging. Always supervise play, charge it with an adult nearby, and don\'t leave it in a cot.</p>',
		)
	);
}

function babyvibes_build_page( $key, array $page, $page_id, array $opts ) {
	$file = BABYVIBES_KIT_DIR . 'templates/babyvibes-' . $key . '.json';
	if ( ! is_readable( $file ) ) {
		return new WP_Error( 'babyvibes_missing', 'template file is missing from the plugin.' );
	}
	$raw = file_get_contents( $file ); // phpcs:ignore WordPress.WP.AlternativeFunctionsLibrary
	$raw = str_replace(
		array( BABYVIBES_PLACEHOLDER_WHATSAPP, BABYVIBES_PLACEHOLDER_EMAIL ),
		array( $opts['whatsapp'], $opts['email'] ),
		$raw
	);
	$data = json_decode( $raw, true );
	if ( ! is_array( $data ) || empty( $data['content'] ) ) {
		return new WP_Error( 'babyvibes_json', 'template file could not be read.' );
	}

	if ( ! $page_id ) {
		$page_id = wp_insert_post(
			array(
				'post_type'   => 'page',
				'post_status' => 'publish',
				'post_title'  => $page['title'],
				'post_name'   => $page['slug'],
			),
			true
		);
		if ( is_wp_error( $page_id ) ) {
			return $page_id;
		}
	}

	update_post_meta( $page_id, '_wp_page_template', 'elementor_header_footer' );
	update_post_meta( $page_id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $page_id, '_elementor_template_type', 'wp-page' );
	if ( defined( 'ELEMENTOR_VERSION' ) ) {
		update_post_meta( $page_id, '_elementor_version', ELEMENTOR_VERSION );
	}

	$settings = isset( $data['page_settings'] ) && is_array( $data['page_settings'] ) ? $data['page_settings'] : array();
	$saved    = false;
	if ( class_exists( '\Elementor\Plugin' ) ) {
		$document = \Elementor\Plugin::$instance->documents->get( $page_id, false );
		if ( $document ) {
			$saved = $document->save(
				array(
					'elements' => $data['content'],
					'settings' => $settings,
				)
			);
		}
	}
	if ( ! $saved ) {
		// Fallback: write the data the way Elementor stores it.
		update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $data['content'] ) ) );
		update_post_meta( $page_id, '_elementor_page_settings', $settings );
	}
	return (int) $page_id;
}

function babyvibes_build_menu( array $pages ) {
	$name = 'BabyVibes main menu';
	$menu = wp_get_nav_menu_object( $name );
	$id   = $menu ? $menu->term_id : wp_create_nav_menu( $name );
	if ( is_wp_error( $id ) ) {
		return;
	}
	foreach ( (array) wp_get_nav_menu_items( $id ) as $item ) {
		wp_delete_post( $item->ID, true );
	}

	$items = array(
		array( 'Home', 'page', $pages['home'] ?? 0 ),
		array( 'Shop the Talking Cactus', 'product', wc_get_product_id_by_sku( BABYVIBES_SKU ) ),
		array( 'About', 'page', $pages['about'] ?? 0 ),
		array( 'FAQ & Delivery', 'page', $pages['faq-delivery'] ?? 0 ),
		array( 'Contact', 'page', $pages['contact'] ?? 0 ),
	);
	foreach ( $items as $i => $item ) {
		if ( ! $item[2] ) {
			continue;
		}
		wp_update_nav_menu_item(
			$id,
			0,
			array(
				'menu-item-title'     => $item[0],
				'menu-item-object'    => $item[1],
				'menu-item-object-id' => (int) $item[2],
				'menu-item-type'      => 'post_type',
				'menu-item-status'    => 'publish',
				'menu-item-position'  => $i + 1,
			)
		);
	}

	// Put it in the theme's main menu slot (Hello Elementor calls it "menu-1").
	$locations = get_registered_nav_menus();
	if ( $locations ) {
		$slot      = isset( $locations['menu-1'] ) ? 'menu-1' : array_key_first( $locations );
		$assigned  = get_theme_mod( 'nav_menu_locations', array() );
		$assigned[ $slot ] = $id;
		set_theme_mod( 'nav_menu_locations', $assigned );
	}
}
