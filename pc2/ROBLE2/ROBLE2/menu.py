from manager import deploy_microservice, list_microservices, stop_microservice, redeploy_microservice, deploy_from_store
from store import save_code, get_codes, get_code, _load_data

def leer_codigo():
    print("Pega el código del microservicio (escribe EOF en una línea vacía para terminar):")
    lineas = []
    while True:
        linea = input()
        if linea.strip() == "EOF":  # cuando el usuario escribe EOF, se corta
            break
        lineas.append(linea)
    return "\n".join(lineas)

def main():
    while True:
        print("\n=== MENÚ DE MICROSERVICIOS ===")
        print("1. Crear microservicio")
        print("2. Listar microservicios")
        print("3. Ver código de un microservicio")
        print("4. Editar microservicio")
        print("5. Eliminar microservicio")
        print("6. Redeploy de todos los microservicios guardados")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre del microservicio: ")
            code = leer_codigo()
            result = deploy_microservice(code, nombre)
            if result:
                save_code(result["name"], code, result["port"])  # guardamos el código
                print(f"Microservicio desplegado en puerto {result['port']}, con el ID: {result['id']} y con el nombre: {result['name']}")
            else:
                print("Error al desplegar microservicio.")

        elif opcion == "2":
            servicios = list_microservices()
            for s in servicios:
                print(f"---{s['nombre']}---{s['name']}---")
                print(f"ID: {s['id']}\nNombre: {s['nombre']}\nPuerto: {s['puerto']}\nURL Base: {s['url base']}\nEndpoints: {s['links']}\n")
                #print(f"--- ID: {s['id']}, Nombre: {s['name']}, Estado: {s['status']}, Puertos: {s['ports']}, Puerto: {s['puerto']}, URL Base: {s['url base']}, Endpoints: {s['endpoints']}")

        elif opcion == "3":
            mid = input("ID del microservicio: ")
            nombre = input("Nombre del microservicio: ")
            code = get_code(f"ms-{mid}-{nombre}")
            if code:
                print("\n--- Código guardado ---")
                print(code)
            else:
                print("No se encontró código para ese ID.")

        elif opcion == "4":
            mid = input("ID del microservicio a editar: ")
            nombre = input("Nombre del microservicio a editar: ")
            name = f"ms-{mid}-{nombre}"
            old_code = get_code(name)
            if not old_code:
                print("No se encontró ese microservicio.")
                continue

            # Buscar el puerto actual del microservicio
            servicios = list_microservices()
            puerto = None
            for s in servicios:
                if s["name"] == name:
                    # Puede que el contenedor esté detenido: verificamos
                    if s["ports"]:
                        puerto = s["ports"]["8000/tcp"][0]["HostPort"]
                    else:
                        puerto = str(5000 + len(servicios))  # fallback
                    break

            print("Código actual:\n", old_code)
            new_code = leer_codigo()

            result = redeploy_microservice(name, new_code, puerto)
            if result:
                save_code(name, new_code, result["port"])  # Se mantiene el mismo ID
                print(f"Microservicio {name} actualizado en puerto {result['port']}")


        elif opcion == "5":
            mid = input("ID del microservicio a eliminar: ")
            nombre = input("Nombre del microservicio a eliminar: ")
            name = f"ms-{mid}-{nombre}"
            stop_microservice(name)
            print("Microservicio eliminado.")

        elif opcion == "6":
            print("Redeploy de todos los microservicios guardados en microservices.json...")
            servicios_guardados = get_codes()

            if not servicios_guardados:
                print("No hay microservicios guardados.")
                continue

            for service_id, data in servicios_guardados.items():
                code = data["code"]
                port = data["port"]

                result = deploy_from_store(service_id, code, port)
                if result:
                    save_code(service_id, code, port)  # aseguramos consistencia
                    print(f"{service_id} levantado en puerto {port}")
                else:
                    print(f"Error al levantar {service_id}")


        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
