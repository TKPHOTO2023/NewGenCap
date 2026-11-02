<?php
/**
 * Front-end: brand styles and small WooCommerce additions.
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
