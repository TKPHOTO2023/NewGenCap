<?php
/**
 * Front-end: brand styles and WooCommerce tweaks for a one-product shop.
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'wp_enqueue_scripts',
	function () {
		wp_enqueue_style(
			'babyvibes-fonts',
			'https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@400;600;800&display=swap',
			array(),
			null
		);
		wp_enqueue_style( 'babyvibes-store', BABYVIBES_KIT_URL . 'assets/store.css', array(), BABYVIBES_KIT_VERSION );
	},
	20
);

if ( ! class_exists( 'WooCommerce' ) && ! in_array( 'woocommerce/woocommerce.php', (array) get_option( 'active_plugins', array() ), true ) ) {
	return;
}

// "Buy now" instead of "Add to cart": with one product, buyers go straight to checkout.
add_filter( 'woocommerce_product_single_add_to_cart_text', 'babyvibes_buy_now_text' );
add_filter( 'woocommerce_product_add_to_cart_text', 'babyvibes_buy_now_text', 10, 2 );
function babyvibes_buy_now_text( $text, $product = null ) {
	if ( $product && ! $product->is_purchasable() ) {
		return $text;
	}
	if ( $product && ! $product->is_in_stock() ) {
		return $text;
	}
	return __( 'Buy now', 'babyvibes' );
}

add_filter(
	'woocommerce_add_to_cart_redirect',
	function ( $url ) {
		return apply_filters( 'babyvibes_skip_cart', true ) ? wc_get_checkout_url() : $url;
	}
);

// One product means "related products" would be empty or repeat itself.
add_action(
	'init',
	function () {
		remove_action( 'woocommerce_after_single_product_summary', 'woocommerce_output_related_products', 20 );
		remove_action( 'woocommerce_after_single_product_summary', 'woocommerce_upsell_display', 15 );
	}
);

// Reassurance under the buy button.
add_action(
	'woocommerce_after_add_to_cart_form',
	function () {
		echo '<ul class="bv-trust">'
			. '<li>' . esc_html__( 'Delivery across South Africa', 'babyvibes' ) . '</li>'
			. '<li>' . esc_html__( 'Secure checkout', 'babyvibes' ) . '</li>'
			. '<li>' . esc_html__( 'Help on WhatsApp', 'babyvibes' ) . '</li>'
			. '</ul>';
	}
);

// While the shop sells a single product, send /shop/ straight to it.
add_action(
	'template_redirect',
	function () {
		if ( ! function_exists( 'is_shop' ) || ! is_shop() || is_search() ) {
			return;
		}
		$ids = wc_get_products(
			array(
				'status' => 'publish',
				'limit'  => 2,
				'return' => 'ids',
			)
		);
		if ( 1 === count( $ids ) ) {
			wp_safe_redirect( get_permalink( $ids[0] ), 302 );
			exit;
		}
	}
);
