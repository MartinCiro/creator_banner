from google import genai
from google.genai import types
from typing import Optional
from re import sub, search, IGNORECASE


class GeminiClient:
    """
    Cliente para generar descripciones de jabones usando Gemini 2.5 Flash
    Versión migrada al nuevo SDK google-genai
    """

    def __init__(self, config):
        self.config = config
        api_key = self._get_api_key()
        
        if not api_key:
            raise ValueError(
                "❌ GEMINI_API_KEY no encontrada. "
                "Asegúrate de tenerla en tu archivo .env"
            )
        
        # Nuevo patrón: cliente centralizado [[16]]
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        self.nombre_jabon = ""
        
        self.base_prompt = """Eres un redactor experto en marketing de cuidado personal. Genera UNA ÚNICA descripción para un jabón.

        REGLAS DE VARIABILIDAD (CLAVE):
        - Cada generación debe iniciar con un enfoque distinto: acción del ingrediente, sensación táctil, resultado visible o rutina de cuidado.
        - Prohíbe estructuras fijas y frases cliché como "nutre profundamente", "deja la piel suave", "radiante", "nuestro jabón" o "ideal para".
        - Rota activamente verbos (purifica, revitaliza, restaura, armoniza, calma, sella) y adjetivos (tersa, luminosa, confortable, equilibrada, fresca, flexible).
        - Integra los beneficios de forma orgánica en una sola oración, sin listarlos mecánicamente.

        RESTRICCIONES:
        1. Longitud estricta: 180 a 220 caracteres (incluye espacios y punto final).
        2. Una sola oración gramatical, sin saltos de línea, exclamaciones ni comillas.
        3. Tono profesional pero cercano.
        4. Menciona 2-3 beneficios concretos y realistas para la piel.
        5. Respuesta única: SOLO el texto de la descripción, sin prefijos ni explicaciones.

        Jabón a describir: {self.nombre_jabon}
        Descripción: """

    def _get_api_key(self) -> Optional[str]:
        if hasattr(self.config, 'gemini_api_key'):
            return self.config.gemini_api_key
        return None

    def generar_descripcion(self, nombre_jabon: str) -> str:
        self.nombre_jabon = nombre_jabon
        try:
            prompt_completo = self.base_prompt + f'"{self.nombre_jabon}"'
            
            # response = self.client.models.generate_content(
            #     model=self.model_name,
            #     contents=prompt_completo,
            #     config=types.GenerateContentConfig(
            #         temperature=0.7,
            #         max_output_tokens=500,
            #     )
            # )
            
            # 🧹 LIMPIEZA: Extraer solo el texto útil
            #descripcion = self._limpiar_respuesta(response.text.strip())
            descripcion = self._limpiar_respuesta(prompt_completo.text.strip())
            
            # Validación de longitud
            if len(descripcion) < 150:
                descripcion = self._expandir_descripcion(descripcion)
            elif len(descripcion) > 250:
                descripcion = self._acortar_descripcion(descripcion)
            
            return self._limpiar_respuesta(descripcion)
            
        except Exception as e:
            return self._descripcion_fallback()
    
    def _expandir_descripcion(self, descripcion_corta: str) -> str:
        try:
            prompt_expandir = f"""
            La siguiente descripción es muy corta (menos de 150 caracteres):
            "{descripcion_corta}"
            Por favor, expándela a unos 200 caracteres manteniendo el mismo estilo profesional.
            Jabón: {self.nombre_jabon}
            """
            # response = self.client.models.generate_content(
            #     model=self.model_name,
            #     contents=prompt_expandir
            # )
            #return response.text.strip()
            return prompt_expandir.strip()
        except:
            return self._descripcion_fallback()
    
    def _acortar_descripcion(self, descripcion_larga: str) -> str:
        primer_punto = descripcion_larga.find('.')
        if 150 < primer_punto < 250:
            return descripcion_larga[:primer_punto + 1]
        return descripcion_larga[:247] + "..." if len(descripcion_larga) > 250 else descripcion_larga
    
    def _descripcion_fallback(self) -> str:
        fallbacks = {
            "avena": "Calma la irritación, hidrata profundamente y protege la barrera natural de la piel. Ideal para pieles sensibles y secas.",
            "carbon": "Purifica profundamente los poros, elimina impurezas y toxinas. Perfecto para pieles grasas y con acné.",
            "miel": "Nutre, hidrata y aporta luminosidad natural. Sus propiedades antibacterianas ayudan a prevenir imperfecciones.",
            "arcilla": "Absorbe el exceso de grasa, minimiza poros y tonifica la piel. Deja una sensación de limpieza profunda.",
        }
        nombre_lower = self.nombre_jabon.lower()
        for key, desc in fallbacks.items():
            if key in nombre_lower:
                return desc
        return "Limpia suavemente mientras cuida tu piel. Sus ingredientes naturales nutren, hidratan y protegen, dejando una sensación de frescura y bienestar duradera."
    
    def _limpiar_respuesta(self, texto: str) -> str:
        """
        Extrae únicamente la descripción limpia, eliminando:
        - Prefijos como 'Aquí tienes...', 'Respuesta:', etc.
        - Comillas envolventes
        - Saltos de línea innecesarios
        """
        
        # 1. Si hay texto entre comillas dobles, extraerlo (prioridad máxima)
        match_comillas = search(r'"([^"]{50,})"', texto)
        if match_comillas:
            return match_comillas.group(1).strip()
        
        # 2. Remover prefijos comunes de respuestas del modelo
        prefijos_a_remover = [
            r'^Aquí tienes.*?:\s*',
            r'^Aquí está.*?:\s*',
            r'^Respuesta:\s*',
            r'^Descripción:\s*',
            r'^Texto generado:\s*',
            r'^Resultado:\s*',
            r'^Por favor, encuentra.*?:\s*',
            r'^Como solicitaste.*?:\s*',
        ]
        
        resultado = texto
        for patron in prefijos_a_remover:
            resultado = sub(patron, '', resultado, flags=IGNORECASE)
        
        # 3. Si hay saltos de línea, tomar solo la primera oración completa
        if '\n' in resultado:
            lineas = [l.strip() for l in resultado.split('\n') if l.strip()]
            # Buscar la primera línea que parezca una descripción válida
            for linea in lineas:
                if len(linea) > 100 and linea[0].isupper():
                    resultado = linea
                    break
        
        # 4. Remover comillas simples o dobles al inicio/final
        resultado = resultado.strip('"\'')
        
        # 5. Normalizar espacios múltiples
        resultado = sub(r'\s+', ' ', resultado).strip()
        
        return resultado