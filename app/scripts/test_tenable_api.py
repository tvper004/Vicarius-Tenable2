#!/usr/bin/env python3
"""
Script de diagnóstico para Tenable.io API
Prueba la conexión y credenciales con la API de Tenable
"""

import requests
import json
import sys

def test_tenable_connection(access_key, secret_key):
    """
    Prueba la conexión con Tenable.io API
    """
    print("=" * 70)
    print("DIAGNÓSTICO DE TENABLE.IO API")
    print("=" * 70)
    
    # Validar longitud de las keys
    print("\n1. Validando formato de credenciales...")
    print(f"   Access Key length: {len(access_key)} caracteres")
    print(f"   Secret Key length: {len(secret_key)} caracteres")
    
    if len(access_key) != 64 or len(secret_key) != 64:
        print("   ⚠️  ADVERTENCIA: Las keys de Tenable.io típicamente tienen 64 caracteres")
        print("   Verifica que copiaste las keys completas")
    else:
        print("   ✓ Longitud de keys correcta")
    
    # Configurar headers
    base_url = "https://cloud.tenable.com"
    headers = {
        "X-ApiKeys": f"accessKey={access_key}; secretKey={secret_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print(f"\n2. URL Base: {base_url}")
    print(f"3. Header X-ApiKeys: accessKey=***{access_key[-8:]}; secretKey=***{secret_key[-8:]}")
    
    # Test 1: Server Info (endpoint público)
    print("\n" + "-" * 70)
    print("TEST 1: Verificando conectividad con Tenable.io")
    print("-" * 70)
    
    try:
        response = requests.get(f"{base_url}/server/properties", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Conexión exitosa con Tenable.io")
            data = response.json()
            print(f"Server Version: {data.get('version', 'N/A')}")
        elif response.status_code == 401:
            print("✗ ERROR 401: Credenciales inválidas")
            print("\nPosibles causas:")
            print("  1. Access Key o Secret Key incorrectos")
            print("  2. Las keys fueron regeneradas y estas están obsoletas")
            print("  3. Formato incorrecto en el header")
            print("\nSolución:")
            print("  - Verifica las keys en Tenable.io → My Account → API Keys")
            print("  - Genera nuevas keys si es necesario")
        elif response.status_code == 403:
            print("✗ ERROR 403: Permisos insuficientes")
            print("El usuario no tiene permisos para acceder a este recurso")
        else:
            print(f"✗ ERROR {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        return False
    
    # Test 2: Workbenches Assets
    print("\n" + "-" * 70)
    print("TEST 2: Probando endpoint /workbenches/assets")
    print("-" * 70)
    
    try:
        url = f"{base_url}/workbenches/assets"
        params = {"date_range": 30}
        
        print(f"URL: {url}")
        print(f"Params: {params}")
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            assets = data.get('assets', [])
            print(f"✓ Éxito! Encontrados {len(assets)} activos")
            
            if len(assets) > 0:
                print("\nPrimer activo de ejemplo:")
                print(json.dumps(assets[0], indent=2))
            else:
                print("\n⚠️  No se encontraron activos en los últimos 30 días")
                print("Esto puede ser normal si no hay escaneos recientes")
                
        elif response.status_code == 401:
            print("✗ ERROR 401: Autenticación fallida")
            print("\nDetalles del error:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
                
        elif response.status_code == 403:
            print("✗ ERROR 403: Sin permisos para ver activos")
            print("\nEl usuario necesita:")
            print("  - Rol: Basic o superior")
            print("  - Permiso: Can View para activos")
            
        else:
            print(f"✗ ERROR {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        return False
    
    # Test 3: User Info
    print("\n" + "-" * 70)
    print("TEST 3: Información del usuario")
    print("-" * 70)
    
    try:
        response = requests.get(f"{base_url}/session", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✓ Usuario: {user_data.get('username', 'N/A')}")
            print(f"  Email: {user_data.get('email', 'N/A')}")
            print(f"  Tipo: {user_data.get('type', 'N/A')}")
            print(f"  Permisos: {user_data.get('permissions', 'N/A')}")
        else:
            print(f"Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"No se pudo obtener información del usuario: {e}")
    
    print("\n" + "=" * 70)
    print("FIN DEL DIAGNÓSTICO")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    print("\n")
    print("Ingresa tus credenciales de Tenable.io")
    print("(Las keys NO se guardarán, solo se usan para la prueba)")
    print("-" * 70)
    
    access_key = input("Access Key: ").strip()
    secret_key = input("Secret Key: ").strip()
    
    if not access_key or not secret_key:
        print("\n✗ Error: Debes proporcionar ambas keys")
        sys.exit(1)
    
    test_tenable_connection(access_key, secret_key)
