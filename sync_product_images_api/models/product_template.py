from odoo import models, fields
from odoo.exceptions import UserError
import requests
import base64
import logging

_logger = logging.getLogger(__name__)

API_URL = "https://chatbot.b4b.com.co/api/v1/products/search-by-codes"
API_KEY = "Vefm4tJF2OeryXIY4wYdynCqz1yTGzOZWsL05Hek"


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_sync_image_from_external_api(self):
        if not self:
            raise UserError("No hay productos seleccionados para procesar.")

        headers = {
            "Content-Type": "application/json",
            "API-KEY": API_KEY,
        }

        sincronizados = 0
        omitidos = []

        for product in self:
            if not product.supplier_internal_reference:
                omitidos.append(f"{product.display_name} (sin referencia proveedor)")
                continue

            payload = {
                "productCodes": product.supplier_internal_reference
            }

            try:
                response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                _logger.error("Error al conectar con la API: %s", str(e))
                raise UserError(f"No se pudo conectar con la API externa: {str(e)}")

            if not data or not isinstance(data, dict) or 'items' not in data:
                omitidos.append(f"{product.display_name} (respuesta inválida de API)")
                continue

            items = data['items']
            product_info = next((p for p in items if p.get('product_code') == product.supplier_internal_reference), None)
            if not product_info:
                omitidos.append(f"{product.display_name} (no se encontró código {product.supplier_internal_reference} en respuesta)")
                continue

            image_url = product_info.get('product_image_url')
            if not image_url:
                omitidos.append(f"{product.display_name} (sin URL de imagen)")
                continue

            try:
                image_response = requests.get(image_url, timeout=10)
                image_response.raise_for_status()
                image_data = base64.b64encode(image_response.content)
                product.write({'image_1920': image_data})
                sincronizados += 1
                _logger.info("Imagen sincronizada desde API: %s (%s)", product.name, product.supplier_internal_reference)
            except Exception as e:
                _logger.error("Error al descargar imagen: %s", str(e))
                omitidos.append(f"{product.display_name} (error al descargar imagen)")

        mensaje = f"✅ Productos sincronizados: {sincronizados}"
        if omitidos:
            mensaje += "\n\n⚠ Omitidos:\n- " + "\n- ".join(omitidos)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sincronización desde API',
                'message': mensaje,
                'type': 'success' if sincronizados else 'warning',
                'sticky': False,
            }
        }