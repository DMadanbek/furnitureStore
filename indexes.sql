
CREATE INDEX idx_order_date ON orders(order_date);

CREATE INDEX idx_customer_name ON customers(customer_name);

CREATE INDEX idx_product_name ON products(product_name);

CREATE INDEX idx_location_region ON locations(region, state);