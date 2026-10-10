(() => {
  "use strict";

  const CART_STORAGE_KEY = "shes-glowing-shopify-cart";
  const grid = document.querySelector("#product-card-1")?.parentElement;
  if (!grid) return;

  const money = (value) => {
    const amount = Number(value?.amount);
    const currency = value?.currencyCode || "USD";
    if (!Number.isFinite(amount)) return "";
    try {
      return new Intl.NumberFormat(undefined, {
        style: "currency",
        currency,
        maximumFractionDigits: 2,
      }).format(amount);
    } catch {
      return `${currency} ${amount.toFixed(2)}`;
    }
  };

  const text = (tag, className, value) => {
    const element = document.createElement(tag);
    element.className = className;
    element.textContent = value || "";
    return element;
  };

  const dialog = document.createElement("dialog");
  dialog.id = "shopify-cart";
  dialog.setAttribute("aria-labelledby", "shopify-cart-title");
  dialog.innerHTML = `
    <section class="sg-cart-panel">
      <header class="sg-cart-header">
        <div>
          <p class="sg-cart-kicker">YOUR GLOW PICKS</p>
          <h2 id="shopify-cart-title">Your bag <span id="sg-cart-count">(0)</span></h2>
        </div>
        <button type="button" class="sg-cart-close" aria-label="Close bag">×</button>
      </header>
      <div id="sg-cart-message" role="status" aria-live="polite"></div>
      <div id="sg-cart-lines"></div>
      <footer class="sg-cart-footer">
        <div class="sg-cart-subtotal"><span>Subtotal</span><strong id="sg-cart-subtotal"></strong></div>
        <p class="sg-cart-note">Shipping and taxes are calculated securely at Shopify checkout.</p>
        <button type="button" id="sg-checkout" class="sg-checkout-button">CHECK OUT</button>
        <button type="button" class="sg-continue-shopping">Continue shopping</button>
      </footer>
    </section>`;
  document.body.append(dialog);

  const lineContainer = dialog.querySelector("#sg-cart-lines");
  const message = dialog.querySelector("#sg-cart-message");
  const checkoutButton = dialog.querySelector("#sg-checkout");
  const subtotal = dialog.querySelector("#sg-cart-subtotal");
  const count = dialog.querySelector("#sg-cart-count");
  let cartId = null;
  let currentCart = null;
  let products = [];

  try {
    cartId = localStorage.getItem(CART_STORAGE_KEY);
  } catch {
    cartId = null;
  }

  async function request(path, payload) {
    const options = payload
      ? {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      : { method: "GET" };
    const response = await fetch(path, { ...options, cache: "no-store" });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(body.error || "That request could not be completed.");
    }
    return body;
  }

  function showMessage(value, isError = false) {
    message.textContent = value || "";
    message.className = value ? (isError ? "sg-cart-error" : "sg-cart-success") : "";
  }

  function setCart(cart) {
    currentCart = cart || null;
    cartId = currentCart?.id || null;
    try {
      if (cartId) localStorage.setItem(CART_STORAGE_KEY, cartId);
      else localStorage.removeItem(CART_STORAGE_KEY);
    } catch {
      // The cart still works for this visit if storage is unavailable.
    }
    renderCart();
    document.querySelectorAll('[data-path="cart"] > span:last-child').forEach((badge) => {
      const quantity = currentCart?.totalQuantity || 0;
      badge.textContent = quantity > 99 ? "99+" : String(quantity);
      badge.setAttribute("aria-label", `${quantity} items in bag`);
    });
    document.querySelectorAll('[data-path="cart"]').forEach((link) => {
      link.setAttribute("aria-label", `Open bag, ${currentCart?.totalQuantity || 0} items`);
    });
  }

  function renderCart() {
    const items = currentCart?.items || [];
    count.textContent = `(${currentCart?.totalQuantity || 0})`;
    subtotal.textContent = money(currentCart?.subtotal) || money({ amount: 0, currencyCode: "USD" });
    lineContainer.replaceChildren();
    checkoutButton.disabled = items.length === 0;
    if (!items.length) {
      lineContainer.append(
        text("p", "sg-cart-empty", "Your bag is waiting for a little glow.")
      );
      return;
    }

    for (const item of items) {
      const row = document.createElement("article");
      row.className = "sg-cart-line";
      if (item.image?.url) {
        const image = document.createElement("img");
        image.src = item.image.url;
        image.alt = item.image.altText || item.title;
        image.loading = "lazy";
        row.append(image);
      }
      const details = document.createElement("div");
      details.className = "sg-cart-item-details";
      details.append(text("h3", "sg-cart-item-title", item.title));
      if (item.variantTitle && item.variantTitle.toLowerCase() !== "default title") {
        details.append(text("p", "sg-cart-variant", item.variantTitle));
      }
      details.append(text("p", "sg-cart-price", money(item.price)));

      const controls = document.createElement("div");
      controls.className = "sg-cart-controls";
      const decrease = text("button", "sg-quantity-button", "−");
      decrease.type = "button";
      decrease.setAttribute("aria-label", `Remove one ${item.title}`);
      decrease.disabled = item.quantity <= 1;
      decrease.addEventListener("click", () => changeLine("update", item, item.quantity - 1));
      const quantity = text("span", "sg-cart-quantity", String(item.quantity));
      const increase = text("button", "sg-quantity-button", "+");
      increase.type = "button";
      increase.setAttribute("aria-label", `Add one ${item.title}`);
      increase.disabled = item.quantity >= 99;
      increase.addEventListener("click", () => changeLine("update", item, item.quantity + 1));
      controls.append(decrease, quantity, increase);
      details.append(controls);

      const remove = text("button", "sg-remove-line", "Remove");
      remove.type = "button";
      remove.addEventListener("click", () => changeLine("remove", item));
      details.append(remove);
      row.append(details);
      lineContainer.append(row);
    }
  }

  async function changeLine(action, item, quantity) {
    showMessage("");
    lineContainer.setAttribute("aria-busy", "true");
    try {
      const result = await request("/api/cart", {
        action,
        cartId,
        lineId: item.lineId,
        quantity,
      });
      setCart(result.cart);
    } catch (error) {
      showMessage(error.message, true);
    } finally {
      lineContainer.removeAttribute("aria-busy");
    }
  }

  function openCart() {
    if (!dialog.open) dialog.showModal();
  }

  dialog.querySelector(".sg-cart-close").addEventListener("click", () => dialog.close());
  dialog.querySelector(".sg-continue-shopping").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });

  function createProductCard(product) {
    const card = document.createElement("article");
    card.className =
      "group flex flex-col bg-surface-container-lowest rounded-3xl p-space-lg shadow-[0_12px_36px_rgba(0,0,0,0.06)] hover:shadow-[0_24px_50px_rgba(164,48,115,0.18)] transition-all duration-300 relative";
    card.dataset.shopHandle = product.handle || "";

    const imageWrap = document.createElement("div");
    imageWrap.className =
      "relative aspect-[4/5] rounded-2xl overflow-hidden bg-surface-container-low mb-space-md";
    if (product.image?.url) {
      const image = document.createElement("img");
      image.src = product.image.url;
      image.alt = product.image.altText || product.title;
      image.loading = "lazy";
      image.className = "w-full h-full object-cover group-hover:scale-105 transition-transform duration-500";
      imageWrap.append(image);
    } else {
      imageWrap.append(text("span", "sg-product-no-image", "She's Glowing"));
    }
    card.append(imageWrap);

    card.append(text(
      "h3",
      "font-headline-sm text-headline-sm text-primary font-bold mb-1 group-hover:text-secondary transition-colors",
      product.title
    ));
    const price = text("p", "font-headline-sm text-headline-sm text-primary font-bold mb-space-sm", "");
    price.dataset.price = "true";
    card.append(price);

    const variants = product.variants || [];
    const available = variants.filter((variant) => variant.availableForSale && variant.id);
    let selectedVariant = available[0] || null;
    let selector = null;
    if (variants.length > 1) {
      selector = document.createElement("select");
      selector.className = "sg-variant-select";
      selector.setAttribute("aria-label", `Choose a variant of ${product.title}`);
      variants.forEach((variant) => {
        if (!variant.id) return;
        const option = document.createElement("option");
        option.value = variant.id;
        option.textContent = variant.availableForSale
          ? (variant.title || "Default")
          : `${variant.title || "Default"} — sold out`;
        option.disabled = !variant.availableForSale;
        selector.append(option);
      });
      if (selectedVariant) selector.value = selectedVariant.id;
      selector.addEventListener("change", () => {
        selectedVariant = available.find((variant) => variant.id === selector.value) || null;
        price.textContent = selectedVariant ? money(selectedVariant.price) : "";
        addButton.disabled = !selectedVariant;
      });
      card.append(selector);
    }
    price.textContent = selectedVariant ? money(selectedVariant.price) : "";

    const addButton = text(
      "button",
      "sg-add-to-bag",
      selectedVariant ? "Add to Bag" : "Sold Out"
    );
    addButton.type = "button";
    addButton.dataset.addToBag = "true";
    addButton.disabled = !selectedVariant;
    addButton.addEventListener("click", async () => {
      if (!selectedVariant || addButton.disabled) return;
      const chosen = selectedVariant;
      addButton.disabled = true;
      addButton.textContent = "Adding…";
      showMessage("");
      try {
        const result = await request("/api/cart", {
          action: "add",
          cartId,
          variantId: chosen.id,
          quantity: 1,
        });
        setCart(result.cart);
        openCart();
        showMessage(`${product.title} added to your bag.`);
      } catch (error) {
        showMessage(error.message, true);
        openCart();
      } finally {
        addButton.disabled = !selectedVariant;
        addButton.textContent = selectedVariant ? "Add to Bag" : "Sold Out";
      }
    });
    card.append(addButton);
    return card;
  }

  function renderCatalog(items, loadError = false) {
    grid.replaceChildren();
    if (loadError) {
      const notice = text(
        "p",
        "sg-catalog-notice",
        "We couldn't load products from Shopify. Check your connection and try again."
      );
      notice.setAttribute("role", "alert");
      const retry = text("button", "sg-catalog-retry", "Try again");
      retry.type = "button";
      retry.addEventListener("click", loadCatalog);
      grid.append(notice, retry);
      return;
    }
    if (!items.length) {
      const notice = text(
        "p",
        "sg-catalog-notice",
        "No products are published to this Shopify storefront yet. Publish products in Shopify and they will appear here."
      );
      notice.setAttribute("role", "status");
      grid.append(notice);
      return;
    }
    items.forEach((product) => grid.append(createProductCard(product)));
  }

  const catalogHeading = grid.closest("section")?.querySelector("h2, h3");
  if (catalogHeading) {
    catalogHeading.id ||= "shopify-product-catalog";
  }
  const featuredTitle = [...document.querySelectorAll("h4")]
    .find((heading) => heading.textContent.trim() === "Celestial Dew Drop");
  const featuredCard = featuredTitle?.closest(".absolute");
  if (featuredCard) featuredCard.style.display = "none";

  function updateFeaturedProduct(product) {
    if (!featuredCard || !featuredTitle) return;
    if (!product) {
      featuredCard.style.display = "none";
      return;
    }
    const variant = (product.variants || []).find((item) => item.availableForSale);
    if (!variant) {
      featuredCard.style.display = "none";
      return;
    }
    featuredCard.style.display = "";
    featuredTitle.textContent = product.title;
    const variantLabel = featuredTitle.parentElement.querySelector("p");
    if (variantLabel) {
      variantLabel.textContent =
        variant.title && variant.title.toLowerCase() !== "default title"
          ? `Option: ${variant.title}`
          : "Available now";
    }
    const featuredPrice = featuredCard.querySelector(":scope > span");
    if (featuredPrice) featuredPrice.textContent = money(variant.price);
  }
  document.addEventListener("click", (event) => {
    const cartLink = event.target.closest('[data-path="cart"]');
    if (cartLink) {
      event.preventDefault();
      openCart();
      return;
    }
    const shopButton = event.target.closest("button");
    if (!shopButton) return;
    const label = shopButton.textContent.trim().toLowerCase();
    if (label.includes("shop the glow drop")) {
      event.preventDefault();
      grid.scrollIntoView({ behavior: "smooth", block: "start" });
    } else if (label.startsWith("shop ")) {
      const requested = label.replace(/^shop\s+/, "").replace(/\s+/g, " ");
      const match = products.find((product) =>
        product.title.toLowerCase().includes(requested)
        || requested.includes(product.title.toLowerCase())
      );
      if (match) {
        event.preventDefault();
        grid.querySelector(`[data-shop-handle="${CSS.escape(match.handle || "")}"]`)
          ?.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  });

  checkoutButton.addEventListener("click", async () => {
    if (!cartId || checkoutButton.disabled) return;
    checkoutButton.disabled = true;
    showMessage("Opening secure Shopify checkout…");
    try {
      const result = await request("/api/checkout", { cartId });
      window.location.assign(result.checkoutUrl);
    } catch (error) {
      showMessage(error.message, true);
      checkoutButton.disabled = false;
    }
  });

  async function refreshCart() {
    if (!cartId) {
      setCart(null);
      return;
    }
    try {
      const result = await request("/api/cart", { action: "get", cartId });
      setCart(result.cart);
    } catch {
      setCart(null);
      showMessage("Your saved bag expired. Add your products again.", true);
    }
  }

  async function loadCatalog() {
    grid.setAttribute("aria-busy", "true");
    grid.replaceChildren(text("p", "sg-catalog-notice", "Loading products from Shopify…"));
    try {
      const result = await request("/api/products");
      products = result.products || [];
      renderCatalog(products);
      updateFeaturedProduct(products.find((product) =>
        product.variants?.some((variant) => variant.availableForSale)
      ));
    } catch {
      renderCatalog([], true);
    } finally {
      grid.removeAttribute("aria-busy");
    }
  }

  refreshCart();
  loadCatalog();
})();
