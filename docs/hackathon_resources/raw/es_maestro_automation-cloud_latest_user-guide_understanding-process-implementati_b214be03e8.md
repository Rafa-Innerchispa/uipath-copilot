# Maestro: descripción general

- **URL:** https://docs.uipath.com/es/maestro/automation-cloud/latest/user-guide/understanding-process-implementatio
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Maestro: descripción general
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
- search Search ​ Idioma translate Español expand_more ​ Iniciar sesión maestro latest false Maestro Automation Cloud · latest - Contraer
- Introducción
- Información general
- Qué obtienes con Maestro
- Quién debe utilizar Maestro
- Cómo encaja Maestro en UiPath
- Introducción a Maestro Case
- Maestro BPMN frente a Maestro Case: cuándo utilizar la gestión de casos
- El ciclo de vida de Maestro Case: desde el desencadenador de eventos hasta la experiencia de la aplicación
- Casos de uso común empresariales
- Caso de uso de origen de préstamos
- Caso de uso de comprar para pagar
- Caso de uso de procesamiento de reclamaciones
- Caso de uso de incorporación de proveedores
- Disponibilidad de la característica de Maestro
- Primeros pasos
- Licencia
- Precios unificados
- Plan flexible
- Requisitos previos
- Estándares de seguridad compatibles
- Página de destino de Maestro
- Inicio
- Instancias de proceso
- Incidentes de proceso
- Prueba Maestro en Playground
- Cree su primer caso con Gestión de casos
- Implementar un proceso simple
- Implementación de un proceso complejo
- Probar procesos de Maestro
- Atajos del teclado
- Modelado de procesos con BPMN
- Comprender el modelado del proceso
- Introducción a BPMN
- Eventos en BPMN
- Tareas en el modelado BPMN
- Puertas de enlace y lógica de flujo
- Marcadores
- Subprocesos y modularidad
- Objetos de datos y almacenes de datos
- Participantes
- Flujos de secuencia
- Elementos compatibles con BPMN
- Patrones y prácticas BPMN
- Flujo y enrutamiento
- Bucles
- Tiempo y recordatorios
- Mensajes y actualizaciones
- Errores y recuperación
- Patrones avanzados
- Abrir el lienzo de modelado
- Modelar tu proceso
- Alinear y conectar elementos BPMN
- Autopilot para Maestro (vista previa)
- Repositorio de procesos
- Modelado de procesos con Gestión de casos
- Diseñar un esquema de entidad de caso persistente
- Definición de claves de caso (sistema frente a externo)
- Establecimiento de contratos de E/S de tareas y reescritura
- Reglas de salida y terminación temprana
- Modelado de etapas primarias y secundarias
- Desencadenar un caso desde Data Fabric
- Implementar personas y permisos a nivel de etapa
- Establecer SLA y reglas de escalada automatizadas
- Configurar un bucle de revisión (reingreso)
- Gestionar instancias de casos activos: pausar, migrar y reintentar
- Diccionario de componentes de gestión de casos de Maestro
- Implementación del proceso
- Comprender la implementación del proceso
- Configurar propiedades y datos
- Configurar la gestión de errores
- Editor de expresiones y variables
- Eventos
- Tareas
- Tarea de servicio
- Tarea de usuario
- Tarea de envío
- Tarea de recepción
- Tarea de regla empresarial (vista previa)
- Tarea de script
- Puertas de enlace
- Implementación multiinstancia
- Subprocesos
- Subproceso de evento
- Proyectos basados en soluciones: configuración especial
- Transición de C# a expresiones de JavaScript
- Integrar sistemas y datos
- Trabajar con archivos en proceso de Maestro
- Operaciones de Data Fabric
- Uso de agentes en Maestro
- Reglas empresariales
- Aplicaciones de proceso
- Depuración
- Simular
- Publicar y actualizar procesos de agente
- Escenarios de implementación comunes
- Extracción y validación de documentos
- Operaciones de proceso
- Comprender las operaciones del proceso
- Trabajar con la gestión de instancias
- ID de instancia personalizado
- Aceleración de instancias
- Filtrado de variables y elementos
- Supervisión de procesos
- Comprender la supervisión de procesos
- Vista de diagrama de instancia
- Panel de supervisión
- Personalizar paneles
- Personalización de alertas
- Crear un panel de Maestro personalizado en Insights
- Alertas
- Notificaciones
- Optimización de procesos
- Comprender la optimización de procesos
- Vista de optimización
- Panel de optimización
- Acceder a la aplicación de optimización de procesos
- Aplicación de optimización de procesos en Process Mining
- Enriquecer la optimización de procesos con datos externos
- Información de referencia
- Preguntas frecuentes de Maestro y ReFramework
- Descargas Inicio Open Dropdown to choose product Maestro ​ Automation Cloud Más reciente Información general Importante : La localización de contenidos recién publicados puede tardar entre una y dos semanas en estar disponible. Guía del usuario de Maestro

 Información general

 link Qué es Maestro ​

 link
 UiPath Maestro™ es una plataforma de orquestación nativa de la nube que unifica la automatización, los agentes de IA y las interacciones humanas en procesos empresariales simplificados de extremo a extremo.

 Permite a las organizaciones modelar y orquestar el trabajo utilizando dos enfoques complementarios: BPMN (modelo y notación de procesos empresariales) para flujos de trabajo estructurados y secuenciales, y gestión de casos para trabajos de larga duración y con muchas excepciones que no se pueden definir completamente por adelantado. Ambos enfoques comparten los mismos servicios de UiPath Platform y pueden funcionar juntos: un caso puede invocar un proceso BPMN como uno de sus tipos de tareas. Para elegir entre los dos enfoques, consulta Cuándo utilizar el proceso BPMN frente a la gestión de casos .

 Maestro también admite la definición de reglas empresariales con DMN (modelo de decisión y notación) y coordina varios actores, incluidos los bots de RPA, las herramientas de IA y las personas, dentro de un solo proceso.

 Este enfoque reemplaza las tareas de automatización desconectadas con flujos de trabajo inteligentes y gobernados que son más fáciles de gestionar, adaptar y escalar.

 Capacidades de Enterprise ​

 link
 Diseñado para uso empresarial, Maestro ofrece supervisión en tiempo real, control centralizado y herramientas de cumplimiento integradas, lo que lo hace ideal para flujos de trabajo complejos y de larga duración. Admite la supervisión de instancias en vivo (pausa, reanudación, reintento), análisis detallados y optimización continua a través de Process Mining. Al proporcionar una única plataforma para orquestar flujos de trabajo agénticos, Maestro ayuda a las organizaciones a mejorar la eficiencia operativa, reducir el trabajo manual y acelerar la transformación digital.

 Este vídeo muestra cómo evoluciona el proceso Origen de préstamos paso a paso: desde un diagrama simple de alto nivel a un flujo impulsado por agentes y completamente orquestado.

 Maestro sirve como mecanismo para mejorar el rendimiento de tu fuerza de trabajo y sistemas automatizados. Combina datos de proceso con tareas y datos en el nivel de automatización para comprender mejor tus procesos.

 Este vídeo demuestra cómo utilizar la vista Gestión de instancias en Maestro para supervisar un flujo de trabajo de procesamiento de facturas.

 Temas relacionados ​

 link

- Cuándo utilizar el proceso BPMN frente a la gestión de casos

- Conceptos básicos de la gestión de casos
 En esta página
- Qué es Maestro ​
- Capacidades de Enterprise ​
- Temas relacionados ​ Help improve this page ¿Te ha resultado útil esta página?

 thumb_up Sí thumb_down No Sig. Qué obtienes con Maestro Conectar

 ¿Necesita ayuda? Soporte

 ¿Quiere aprender? UiPath Academy

 ¿Tiene alguna pregunta? Foro de UiPath

 Manténgase actualizado