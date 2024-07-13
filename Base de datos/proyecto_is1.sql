-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-07-2024 a las 04:42:05
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_is1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `email` varchar(50) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `fecha_registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre`, `apellido`, `fecha_nacimiento`, `email`, `telefono`, `direccion`, `fecha_registro`) VALUES
(1, 'Luis', 'Melgarr', '2024-07-27', 'luis.melgar@ujcv.edu.hn', '12345678', 'tegucigalpa', '2024-07-22'),
(2, 'w', 'w', '0000-00-00', 'w', 'w', 'w', '0000-00-00'),
(3, 'as', 'as', '2024-07-19', 'grupo123@gmail.com', '32225724', 'tegucigalpa', '2024-07-22'),
(4, 'luis', 'Melgarr', '2024-07-10', 'luisanamc09@yahoo.com', 'qwertyui', 'tegucigalpa', '2024-07-15'),
(5, 'luis', 'Melgar', '2024-07-05', 'luis.melgar@ujcv.edu.hn', 'qwertyas', 'tegucigalpa', '2024-07-20'),
(6, 'luis', 'Melgar', '2024-07-26', 'luis.melgar@ujcv.edu.hn', 'aszxcvfd', 'tegucigalpa', '2024-07-26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devolucion`
--

CREATE TABLE `devolucion` (
  `id` int(100) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `devolucion`
--

INSERT INTO `devolucion` (`id`, `correo`, `nombre`, `estado`, `descripcion`, `fecha`) VALUES
(1, 'luis@gmail.com', 'luis', 'malo', 'Es un fresco ', '2024-07-26'),
(2, 's@swqe', 'leroy', 'medio', 'Herramienta para tostar pan', '2024-07-12'),
(3, 'luis@gmail.com', 'luis', 'malo', '1234567890987', '2024-07-26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(6) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `puesto_de_trabajo` varchar(50) NOT NULL,
  `fecha_contratacion` date NOT NULL,
  `sucursal` varchar(50) NOT NULL,
  `salario` decimal(10,0) NOT NULL,
  `email` varchar(50) NOT NULL,
  `telefono` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `nombre`, `apellido`, `fecha_nacimiento`, `puesto_de_trabajo`, `fecha_contratacion`, `sucursal`, `salario`, `email`, `telefono`) VALUES
(1, 'luis', 'Melgar', '2003-08-30', 'Jefe', '2024-07-01', 'Tegucigalpa', 35700, 'luis.melgar@ujcv.edu.hn', '12345678'),
(2, 'Juan', 'Delgado', '1998-08-18', 'Vendedor', '2024-03-06', 'Cortes', 20000, 'juandelgado@gmail.com', '77668594');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `encuestas`
--

CREATE TABLE `encuestas` (
  `id_encuesta` int(4) NOT NULL,
  `cliente` varchar(20) NOT NULL,
  `fecha` date NOT NULL,
  `puntuacion` int(3) NOT NULL,
  `comentarios` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `encuestas`
--

INSERT INTO `encuestas` (`id_encuesta`, `cliente`, `fecha`, `puntuacion`, `comentarios`) VALUES
(1, 'luis', '2024-07-25', 9, 'es muy bueno'),
(3, 'Armando', '2024-07-27', 5, 'nivel medio'),
(4, 'julio', '2024-07-19', 7, 'medio trabajo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gasto`
--

CREATE TABLE `gasto` (
  `Id_gasto` int(100) NOT NULL,
  `fecha_gasto` int(50) NOT NULL,
  `monto` int(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gasto`
--

INSERT INTO `gasto` (`Id_gasto`, `fecha_gasto`, `monto`, `descripcion`) VALUES
(1, 2024, 30000, 'se gasto en neveras grandes'),
(2, 2024, 20000, 'de urgenciua'),
(3, 2024, 3, 'a.a'),
(4, 2024, 0, 'Herramienta para tostar pan');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `impuestos`
--

CREATE TABLE `impuestos` (
  `id_impuestos` int(100) NOT NULL,
  `nombre_producto` varchar(50) NOT NULL,
  `precio_base` decimal(20,0) NOT NULL,
  `tasa_impuesto` decimal(20,0) NOT NULL,
  `impuesto_calculado` decimal(15,0) NOT NULL,
  `precio_final` decimal(20,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `impuestos`
--

INSERT INTO `impuestos` (`id_impuestos`, `nombre_producto`, `precio_base`, `tasa_impuesto`, `impuesto_calculado`, `precio_final`) VALUES
(1, 'jabon', 200, 10, 210, 210);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_inventario` int(100) NOT NULL,
  `nombre_del_producto` varchar(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `cantidad_en_stock` int(100) NOT NULL,
  `stock_minimo` int(100) NOT NULL,
  `stock_maximo` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_inventario`, `nombre_del_producto`, `descripcion`, `cantidad_en_stock`, `stock_minimo`, `stock_maximo`) VALUES
(1, 'mountain dew', 'Es un fresco ', 30, 5, 50),
(2, 'Tostadoras', 'Herramienta para tostar pan', 100, 35, 150),
(3, 'Refrigerador', 'Refrigerador grande', 90, 10, 120),
(8, 'cucharas', 'son de metal grande', 300, 20, 500),
(10, 'sss', 'asdfghjkloiuytr', 34, 30, 40),
(11, 'aas', 'sssssssssssssssssssssssssssssssssssss', 20, 10, 40);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `Id_producto` int(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `categoria` varchar(50) NOT NULL,
  `precio` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`Id_producto`, `nombre`, `categoria`, `precio`) VALUES
(1, 'estufa', 'hogar', 6000),
(2, 'Nevera', 'cocina', 1700),
(3, 'Micro', 'cocina', 1200),
(4, 'refri', 'cocina', 9000),
(8, 'nosedenuevo', 'nosee', 99),
(9, 'estufeeeeeeee', 'hogarmas nos e que poner', 7000),
(10, 'mesa', 'hogar', 7300);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `promociones_y_descuentos`
--

CREATE TABLE `promociones_y_descuentos` (
  `id_promocion` int(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `valor` decimal(50,0) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date NOT NULL,
  `estado_promocion` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `Nombre_del_proveedor` varchar(50) NOT NULL,
  `Contacto` text NOT NULL,
  `Producto_Servicio` text NOT NULL,
  `Historial_de_desempeño` text NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_marca` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `Nombre_del_proveedor`, `Contacto`, `Producto_Servicio`, `Historial_de_desempeño`, `id_pedido`, `id_marca`) VALUES
(1, 'Cualquiera', 'nose', 'lavar', 'medio', 12, 1234),
(2, 'Lg', 'Juan Ramiro', 'Venta de electrodomesticos', 'Alto', 4433, 6577),
(3, 'better kitchen', 'Rubilio Castillo', 'vendero de cocinas', 'Medio', 9988, 7881),
(6, '12', '1', '1', '1', 1, 1),
(9, 'cocineros', 'sergio peña', 'vendero de tenedores', 'bajo', 1234, 4321);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguridad`
--

CREATE TABLE `seguridad` (
  `id_configuracion` int(11) NOT NULL,
  `nombre_de_configuracion` varchar(15) NOT NULL,
  `descripcion` varchar(30) NOT NULL,
  `estado_config` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `seguridad`
--

INSERT INTO `seguridad` (`id_configuracion`, `nombre_de_configuracion`, `descripcion`, `estado_config`) VALUES
(1, 'Seguridad red', 'Complicacion red', 'activo'),
(2, 'servidores', 'configuracion', 'activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ticket`
--

CREATE TABLE `ticket` (
  `id_ticket` int(100) NOT NULL,
  `nombre_cliente` varchar(30) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `asunto` varchar(100) NOT NULL,
  `estado` varchar(100) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ticket`
--

INSERT INTO `ticket` (`id_ticket`, `nombre_cliente`, `correo`, `asunto`, `estado`, `fecha`) VALUES
(1, 'luis', 'luis@gmail.com', 'nose', 'nose', '2024-07-20'),
(2, './/./', '.@gm', '..//', '..//', '2024-07-26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transaccion`
--

CREATE TABLE `transaccion` (
  `id_transaccion` int(100) NOT NULL,
  `nombre_cliente` varchar(30) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `monto` int(100) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `transaccion`
--

INSERT INTO `transaccion` (`id_transaccion`, `nombre_cliente`, `correo`, `descripcion`, `monto`, `fecha`) VALUES
(1, 'luis', 'luis@gmail.com', 'Herramienta para tostar pan', 100000, '2024-07-19'),
(2, 'rodri', 'rodri@gmail.com', 'pago las deudas del mes', 20000, '2024-07-24');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(100) NOT NULL,
  `primer_nombre` varchar(20) NOT NULL,
  `primer_apellido` varchar(20) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `usuario_activo` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `primer_nombre`, `primer_apellido`, `correo`, `password`, `usuario_activo`) VALUES
(1, 'luis', 'melgar', 'luis@gmail.com', 'scrypt:32768:8:1$UxEQQW9lLdbEra7D$ab38988d699b2598', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `devolucion`
--
ALTER TABLE `devolucion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`);

--
-- Indices de la tabla `encuestas`
--
ALTER TABLE `encuestas`
  ADD PRIMARY KEY (`id_encuesta`);

--
-- Indices de la tabla `gasto`
--
ALTER TABLE `gasto`
  ADD PRIMARY KEY (`Id_gasto`);

--
-- Indices de la tabla `impuestos`
--
ALTER TABLE `impuestos`
  ADD PRIMARY KEY (`id_impuestos`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_inventario`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`Id_producto`);

--
-- Indices de la tabla `promociones_y_descuentos`
--
ALTER TABLE `promociones_y_descuentos`
  ADD PRIMARY KEY (`id_promocion`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `seguridad`
--
ALTER TABLE `seguridad`
  ADD PRIMARY KEY (`id_configuracion`);

--
-- Indices de la tabla `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id_ticket`);

--
-- Indices de la tabla `transaccion`
--
ALTER TABLE `transaccion`
  ADD PRIMARY KEY (`id_transaccion`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `devolucion`
--
ALTER TABLE `devolucion`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `encuestas`
--
ALTER TABLE `encuestas`
  MODIFY `id_encuesta` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `gasto`
--
ALTER TABLE `gasto`
  MODIFY `Id_gasto` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `impuestos`
--
ALTER TABLE `impuestos`
  MODIFY `id_impuestos` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_inventario` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `Id_producto` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `promociones_y_descuentos`
--
ALTER TABLE `promociones_y_descuentos`
  MODIFY `id_promocion` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `seguridad`
--
ALTER TABLE `seguridad`
  MODIFY `id_configuracion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `ticket`
--
ALTER TABLE `ticket`
  MODIFY `id_ticket` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `transaccion`
--
ALTER TABLE `transaccion`
  MODIFY `id_transaccion` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
