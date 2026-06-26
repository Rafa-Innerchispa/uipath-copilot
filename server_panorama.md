# 🖥️ SERVER PANORAMA & PLANO GENERAL DE INFRAESTRUCTURA
# PROYECTO ACTUAL: uipath-copilot
# HACKATHON: UiPath AgentHack 2026
# NOTA: Este mapa se auto-genera en caliente para garantizar datos reales del entorno.

Este documento contiene la radiografía operativa del servidor y las directrices estructurales para el desarrollo de este módulo. Cualquier agente de IA, IDE o desarrollador debe leer este archivo antes de inicializar código para garantizar el aislamiento del entorno.

---

## 📊 1. RECURSOS DEL SISTEMA (HOST: 192.168.1.4 | USUARIO: rlopez)
* **Memoria RAM Disponible:** 25.17 GB (Para inferencia y ejecución de contenedores).
* **Modelos de IA Locales Instalados (Puerto 11434):** starcoder2:3b, qwen2.5:14b-instruct-q4_K_M, llama3.1:8b, codellama:7b, neural-chat:7b, llava:7b, qwen2.5-coder:7b, phi3.5:3.8b, mistral:7b-instruct-v0.3-q4_K_M, qwen2.5:7b, nomic-embed-text:latest

---

## 🚫 2. MATRIZ DE PUERTOS PROHIBIDOS (ACTUALMENTE EN USO)
No asigne ninguno de los siguientes puertos a los nuevos servicios para evitar colisiones:
`22, 53, 3000, 3001, 4000, 4040, 5173, 5180, 5188, 5190, 5432, 5433, 5678, 6333, 8081, 8082, 8090, 8091, 8095, 8096, 8100, 8123, 8200, 8800, 9000, 9001, 9090, 9095, 9222, 11434, 18554, 18555, 20241, 24678, 27017, 32843, 32847, 32861, 32983, 33205, 33213, 33277, 33323, 33385, 33411, 33583, 33587, 33611, 33621, 33627, 33673, 33749, 33775, 33851, 33889, 33915, 34019, 34021, 34053, 34087, 34097, 34119, 34127, 34253, 34277, 34307, 34347, 34503, 34527, 34569, 34705, 34837, 34861, 34887, 34897, 35107, 35259, 35269, 35341, 35377, 35407, 35447, 35493, 35509, 35545, 35659, 35663, 35667, 35685, 35723, 35773, 35815, 35817, 35983, 36037, 36075, 36085, 36135, 36211, 36229, 36285, 36483, 36489, 36523, 36545, 36549, 36615, 36633, 36687, 36731, 36771, 36859, 36909, 36925, 37055, 37113, 37115, 37145, 37165, 37209, 37271, 37503, 37621, 37679, 37765, 37835, 37853, 37855, 37915, 37963, 37985, 38309, 38365, 38441, 38467, 38469, 38473, 38497, 38525, 38549, 38567, 38605, 38727, 38729, 38791, 38827, 38837, 38869, 38895, 38903, 38907, 38911, 39063, 39183, 39223, 39255, 39339, 39395, 39421, 39431, 39521, 39611, 39639, 39657, 39691, 39719, 39797, 40037, 40133, 40151, 40209, 40357, 40365, 40387, 40527, 40549, 40595, 40683, 40697, 40743, 40811, 40841, 40859, 40865, 40939, 41011, 41041, 41159, 41459, 41515, 41581, 41595, 41601, 41839, 41913, 41989, 42077, 42103, 42105, 42165, 42373, 42545, 42567, 42599, 42623, 42627, 42695, 42703, 42771, 42777, 42803, 42845, 43009, 43077, 43089, 43099, 43107, 43147, 43155, 43217, 43227, 43233, 43249, 43627, 43693, 43705, 43833, 43839, 43855, 43949, 43965, 44049, 44051, 44065, 44167, 44201, 44233, 44259, 44269, 44271, 44323, 44333, 44381, 44427, 44467, 44513, 44543, 44715, 44751, 44853, 44857, 44937, 44973, 45017, 45033, 45073, 45213, 45257, 45273, 45351, 45409, 45517, 45539, 45587, 45615, 45641, 45657, 45665, 45747, 45789, 45801, 45833, 45921, 45947, 45979, 46061, 46087, 46127, 46147, 46199, 46207, 46209, 46225, 46303, 46311, 46379, 46381, 46407, 46437, 46477, 46483, 46513, 46515, 46533, 46555, 46589, 46613, 46657, 46659, 46735, 46745, 46749, 46795, 46851, 46875`

---

## 🚀 3. ASIGNACIÓN ASÍNCRONA PARA ESTE PROYECTO
* **Puerto Host Reservado:** **8097**
* *Directiva:* Configure el archivo de configuración del backend (FastAPI/Uvicorn) y el Dockerfile para exponer la aplicación estrictamente a través de este puerto mapeado.

---

## 📦 4. COMPONENTES ESTRUCTURALES DE LA ARQUITECTURA (INNEROS CHASIS)
Para mantener la coherencia del ecosistema, este proyecto debe heredar la topología modular estándar:
1. **Capa de Datos:** Conexión asíncrona a PostgreSQL central (Puerto 5432). Se debe aislar el entorno ejecutando automáticamente la sentencia `CREATE DATABASE IF NOT EXISTS uipath_copilot`.
2. **Capa de Telemetría Móvil:** Enrutamiento de alertas críticas en formato Markdown hacia el administrador por medio del gateway de Evolution API (Puertos 5180/5190).
3. **Capa de Inferencia:** Orquestador híbrido preparado para interactuar con Ollama local o con enrutadores externos según el track del desarrollo.

---

## 🛠️ 5. REGLAS DE DESPLIEGUE CONTINUO
* Todo desarrollo debe vivir en su propio Branch de Git.
* La aplicación final debe ser empaquetada en un contenedor Docker independiente, permitiendo que se apague o encienda sin afectar a las otras verticales de negocio que corren en el host.
