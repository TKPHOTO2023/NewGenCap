<?php
/**
 * Plugin Name:       BabyVibes Store Kit
 * Description:       Sets up the BabyVibes shop (Talking Cactus product, Elementor pages, menu, homepage) and adds the BabyVibes look and one-product checkout tweaks to WooCommerce.
 * Version:           1.0.0
 * Requires at least: 6.2
 * Requires PHP:      7.4
 * Author:            BabyVibes
 * Text Domain:       babyvibes
 */

defined( 'ABSPATH' ) || exit;

define( 'BABYVIBES_KIT_VERSION', '1.0.0' );
define( 'BABYVIBES_KIT_DIR', plugin_dir_path( __FILE__ ) );
define( 'BABYVIBES_KIT_URL', plugin_dir_url( __FILE__ ) );
define( 'BABYVIBES_SKU', 'BV-TC-001' );

require_once BABYVIBES_KIT_DIR . 'includes/store.php';

if ( is_admin() ) {
	require_once BABYVIBES_KIT_DIR . 'includes/setup.php';
}

add_filter(
	'plugin_action_links_' . plugin_basename( __FILE__ ),
	function ( $links ) {
		array_unshift( $links, '<a href="' . esc_url( admin_url( 'admin.php?page=babyvibes-setup' ) ) . '">' . esc_html__( 'Set up store', 'babyvibes' ) . '</a>' );
		return $links;
	}
);
