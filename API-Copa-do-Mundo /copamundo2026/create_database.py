#!/usr/bin/env python3
"""
Script para criar o banco de dados PostgreSQL para o projeto Copa do Mundo
"""

import psycopg2
from psycopg2 import sql
import sys

# Configurações de conexão
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'copamundo2026'

def create_database():
    """Cria o banco de dados se não existir"""
    try:
        # Conectar ao banco de dados padrão 'postgres'
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'
        )
        
        # Configurar autocommit para criar database
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar se o banco já existe
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
            [DB_NAME]
        )
        
        if cursor.fetchone():
            print(f"✓ Banco de dados '{DB_NAME}' já existe!")
        else:
            # Criar o banco
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DB_NAME)
                )
            )
            print(f"✓ Banco de dados '{DB_NAME}' criado com sucesso!")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"✗ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

if __name__ == '__main__':
    if create_database():
        print("\nAgora execute: python manage.py migrate")
        sys.exit(0)
    else:
        sys.exit(1)
