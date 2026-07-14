const { DataTypes } = require('sequelize');
const sequelize = require('../database/connection');

const Livro = sequelize.define(
  'Livro',
  {
    titulo: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    autor: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    editora: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    isbn: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    preco: {
      type: DataTypes.DECIMAL(10, 2),
      allowNull: false,
    },
    estoque: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    ano_publicacao: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
  },
  {
    tableName: 'livros',
  }
);

module.exports = Livro;