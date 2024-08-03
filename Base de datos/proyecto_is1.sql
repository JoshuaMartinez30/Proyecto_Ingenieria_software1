-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-07-2024 a las 06:40:25
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
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre_categoria` varchar(20) NOT NULL,
  `Descripcion` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `fecha_registro` date NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `documento` varchar(14) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre`, `apellido`, `fecha_nacimiento`, `email`, `telefono`, `direccion`, `fecha_registro`, `tipo`, `documento`) VALUES
(1, 'Luisyoyo', 'Melgajo', '2024-07-27', 'luis.melgar@ujcv.edu.hn', '12345678', 'tegucigalpa', '2024-07-22', '', ''),
(2, 'thomas', 'felix', '1979-07-19', 'felix@juan@gmail.com', '12342534', 'sanpedro', '2024-08-07', '', ''),
(3, 'as', 'as', '2024-07-19', 'grupo123@gmail.com', '32225724', 'tegucigalpa', '2024-07-22', '', ''),
(4, 'luis', 'Melgarr', '2024-07-10', 'luisanamc09@yahoo.com', 'qwertyui', 'tegucigalpa', '2024-07-15', '', ''),
(5, 'luis', 'Melgar', '2024-07-05', 'luis.melgar@ujcv.edu.hn', 'qwertyas', 'tegucigalpa', '2024-07-20', '', ''),
(6, 'jack', 'Melgar', '2024-07-26', 'luis.melgar@ujcv.edu.hn', '3344557788', 'tegucigalpa', '2024-07-26', '', ''),
(7, 'luis', 'Melgar', '2024-08-02', 'raglemsiul3003@gmail.com', '87798669', 'tegucigalpa', '2024-07-23', '', ''),
(8, 'ana', 'Melgar', '2024-07-17', 'grupo123@gmail.com', '12345678', 'tegucigalpa', '2024-07-19', '', ''),
(9, 'fabio', 'fernandez', '2024-07-05', 'luismelgar345@yahoo.es', '87798669', 'tegucigalpa', '2024-08-02', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documentacion`
--

CREATE TABLE `documentacion` (
  `id_documento` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `documento` varchar(14) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `direccion` varchar(40) DEFAULT NULL,
  `ciudad` varchar(40) DEFAULT NULL,
  `pais` varchar(40) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `fecha_propuesta` timestamp NOT NULL DEFAULT current_timestamp(),
  `id_cliente` int(11) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `id_gestion` int(11) DEFAULT NULL,
  `id_mantenimiento` int(11) DEFAULT NULL,
  `id_mejora` int(11) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `telefono` varchar(15) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `documento` varchar(14) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `nombre`, `apellido`, `fecha_nacimiento`, `puesto_de_trabajo`, `fecha_contratacion`, `sucursal`, `salario`, `email`, `telefono`, `tipo`, `documento`) VALUES
(1, 'luis', 'Melgar', '2003-08-30', 'Jefe', '2024-07-01', 'Tegucigalpa', 35700, 'luis.melgar@ujcv.edu.hn', '12345678', '', ''),
(2, 'Juan', 'Delgado', '1998-08-18', 'Vendedor', '2024-03-06', 'Cortes', 20000, 'juandelgado@gmail.com', '77668594', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `encuestas`
--

CREATE TABLE `encuestas` (
  `id_encuesta` int(4) NOT NULL,
  `documento` varchar(13) NOT NULL,
  `fecha` date NOT NULL,
  `puntuacion` int(3) NOT NULL,
  `comentarios` varchar(50) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `encuestas`
--

INSERT INTO `encuestas` (`id_encuesta`, `documento`, `fecha`, `puntuacion`, `comentarios`, `id_cliente`, `id_empleado`) VALUES
(1, 'luis', '2024-07-25', 10, 'es muy bueno', NULL, NULL),
(3, 'Armando', '2024-07-27', 4, 'nivel medioo', NULL, NULL),
(4, 'douglas', '2024-07-19', 7, 'medio trabajo', NULL, NULL),
(5, 'pablin', '2024-07-23', 7, 'es muy bueno', NULL, NULL),
(6, 'Andrea', '2024-07-16', 8, 'exelente ', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipo`
--

CREATE TABLE `equipo` (
  `id_equipo` int(11) NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `Modelo` varchar(10) NOT NULL,
  `numero_serie` varchar(20) NOT NULL,
  `estado` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `equipo`
--

INSERT INTO `equipo` (`id_equipo`, `tipo`, `Modelo`, `numero_serie`, `estado`) VALUES
(2222, 'automatico', 'viejo', '8647', 'en_reparac'),
(3030, 'electrico', 'nuevo', '1235', 'bueno');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestion_almacenes`
--

CREATE TABLE `gestion_almacenes` (
  `id_gestion` int(11) NOT NULL,
  `ciudad` varchar(30) NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  `Telefono` varchar(9) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `documento` varchar(14) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestion_almacenes`
--

INSERT INTO `gestion_almacenes` (`id_gestion`, `ciudad`, `id_sucursal`, `Telefono`, `tipo`, `documento`) VALUES
(1, 'New York', 1, '2125-1234', '', 'D45678901'),
(2, 'Los Angeles', 2, '3105-6789', '', 'D98765432'),
(3, 'Chicago', 3, '3125-4321', '', 'D12345678'),
(4, 'Houston', 4, '7135-5678', '', 'D87654321'),
(5, 'New York', 6, '4165-3456', '', 'etc'),
(7, 'Bogota', 7, '5551-2345', '', 'etc'),
(8, 'MonteVideo', 3, '3125-8765', '', 'etc'),
(9, 'america', 5, '3055-6789', '', 'etc'),
(10, 'Manhattan', 7, '5551-2345', '', 'etc'),
(11, 'america', 7, '5551-2345', '', 'etc'),
(15, 'Philadelphia', 5, '2155-6789', '', 'D11223344');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ideas_mejora`
--

CREATE TABLE `ideas_mejora` (
  `id_mejora` int(7) NOT NULL,
  `fecha_propuesta` date NOT NULL,
  `descripcion_idea` text NOT NULL,
  `estado` varchar(50) NOT NULL,
  `fecha_implementacion` date NOT NULL,
  `descripcion_implementacion` text NOT NULL,
  `fecha_evaluacion` date NOT NULL,
  `impacto` text NOT NULL,
  `indicadores_rendimiento` text NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `documento` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ideas_mejora`
--

INSERT INTO `ideas_mejora` (`id_mejora`, `fecha_propuesta`, `descripcion_idea`, `estado`, `fecha_implementacion`, `descripcion_implementacion`, `fecha_evaluacion`, `impacto`, `indicadores_rendimiento`, `tipo`, `documento`) VALUES
(1, '2024-07-23', 'Hacer un listado de errores', 'Revisado', '2024-07-31', 'Armado de ideas', '2024-07-31', 'a futuro', 'alto', '', '5404'),
(2, '2024-07-24', 'mejorar interfaz usuario', 'No Revisado', '2024-08-01', 'diseño y desarrollo', '2024-08-01', 'a futuro', 'medio', '', '5405'),
(3, '2024-07-25', 'optimizar base de datos', 'Revisado', '2024-08-02', 'implementación de índices', '2024-08-02', 'a futuro', 'alto', '', '5406');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_inventario` int(100) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `cantidad_en_stock` int(100) NOT NULL,
  `stock_minimo` int(100) NOT NULL,
  `stock_maximo` int(100) NOT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_inventario`, `descripcion`, `cantidad_en_stock`, `stock_minimo`, `stock_maximo`, `id_producto`, `id_categoria`) VALUES
(1, 'Es un fresco ', 30, 5, 50, NULL, NULL),
(2, 'Herramienta para tostar pan', 100, 35, 150, NULL, NULL),
(3, 'Refrigerador grande', 90, 10, 133, NULL, NULL),
(8, 'son de metal grande', 300, 20, 500, NULL, NULL),
(10, 'asdfghjkloiuytr', 34, 30, 40, NULL, NULL),
(11, 'cartones grandes', 20, 10, 40, NULL, NULL),
(12, 'Herramienta para tostar pan', 2, 1, 33, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mantenimiento_equipo`
--

CREATE TABLE `mantenimiento_equipo` (
  `id_mantenimiento` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `detalles` varchar(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `tipo_documento` varchar(50) NOT NULL,
  `documento` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mantenimiento_equipo`
--

INSERT INTO `mantenimiento_equipo` (`id_mantenimiento`, `id_equipo`, `fecha`, `tipo`, `detalles`, `estado`, `tipo_documento`, `documento`) VALUES
(1, 2222, '2024-07-26', 'electrico', 'esta malo', 'malo', '', '0801200411790'),
(3, 3030, '2024-07-26', 'mecanico', 'reparado', 'bueno', '', '0801200411790');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `Id_producto` int(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  `original_precio` decimal(10,2) DEFAULT NULL,
  `precio_descuento` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `promociones_y_descuentos`
--

CREATE TABLE `promociones_y_descuentos` (
  `id_promocion` int(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
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
  `nombre_compañia` varchar(20) NOT NULL,
  `Telefono` varchar(10) NOT NULL,
  `Ciudad` varchar(20) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `Documento` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `Nombre_del_proveedor`, `Contacto`, `Producto_Servicio`, `Historial_de_desempeño`, `id_pedido`, `nombre_compañia`, `Telefono`, `Ciudad`, `tipo`, `Documento`) VALUES
(1, 'faratets', 'nose', 'lavar', 'medio', 12, '', '', '', '', ''),
(2, 'Lg', 'Juan Ramiro', 'Venta de electrodomesticos', 'Alto', 4433, '', '', '', '', ''),
(3, 'better kitchen', 'Rubilio Castillo', 'vendero de cocinas', 'Medio', 9988, '', '', '', '', ''),
(9, 'cocineros', 'sergio peña', 'vendero de tenedores', 'bajo', 1234, '', '', '', '', ''),
(10, 'bears', 'thoms', 'gerente', 'medio', 9982, '', '', '', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursales`
--

CREATE TABLE `sucursales` (
  `id_sucursal` int(11) NOT NULL,
  `Ciudad` varchar(20) NOT NULL,
  `Telefono` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sucursales`
--

INSERT INTO `sucursales` (`id_sucursal`, `Ciudad`, `Telefono`) VALUES
(1, 'New York', '2125-1234'),
(2, 'Los Angeles', '2135-5678'),
(3, 'Chicago', '3125-8765'),
(4, 'Houston', '7135-4321'),
(5, 'Miami', '3055-6789'),
(6, 'Toronto', '4165-3456'),
(7, 'Mexico City', '5551-2345'),
(17, 'Bogota', '4567-6522');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ticket`
--

CREATE TABLE `ticket` (
  `id_ticket` int(100) NOT NULL,
  `documento` varchar(13) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `asunto` varchar(100) NOT NULL,
  `estado` varchar(100) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ticket`
--

INSERT INTO `ticket` (`id_ticket`, `documento`, `correo`, `asunto`, `estado`, `fecha`) VALUES
(1, 'luis', 'luis@gmail.com', 'nose', 'nose', '2024-07-20'),
(2, './/./', '.@gm', '..//', '..//', '2024-07-26'),
(3, 'juan', 'luis@gmail.com', 'noseque poner s', 'nose que p', '2024-07-26'),
(4, 'pablo', 'luis@gmail.com', 'cotizacion', 'pendiente', '2024-07-25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transportistas`
--

CREATE TABLE `transportistas` (
  `id_transportista` int(11) NOT NULL,
  `nombre_empresa` varchar(40) NOT NULL,
  `Telefono` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `usuario_activo` int(100) NOT NULL,
  `super_usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `primer_nombre`, `primer_apellido`, `correo`, `password`, `usuario_activo`, `super_usuario`) VALUES
(3, 'grupo', 'grupo', 'grupo123@gmail.com', 'scrypt:32768:8:1$nvzVIR1NLZlbIOD1$eab8a0ba1dd1bf97', 1, NULL),
(5, 'Joshua', 'Martinez', 'joshuamartinez8723@gmail.com', 'scrypt:32768:8:1$XDQfazbsC56HELw1$6fb1adb2dab17a8f', 1, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `documentacion`
--
ALTER TABLE `documentacion`
  ADD PRIMARY KEY (`id_documento`),
  ADD UNIQUE KEY `documento` (`documento`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `documentacion_FK` (`id_cliente`),
  ADD KEY `documentacion_FK_1` (`id_empleado`),
  ADD KEY `documentacion_FK_2` (`id_gestion`),
  ADD KEY `documentacion_FK_3` (`id_mantenimiento`),
  ADD KEY `documentacion_FK_4` (`id_mejora`),
  ADD KEY `documentacion_FK_5` (`id_proveedor`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`);

--
-- Indices de la tabla `encuestas`
--
ALTER TABLE `encuestas`
  ADD PRIMARY KEY (`id_encuesta`),
  ADD KEY `encuestas_FK` (`id_empleado`),
  ADD KEY `encuestas_FK_1` (`id_cliente`);

--
-- Indices de la tabla `equipo`
--
ALTER TABLE `equipo`
  ADD PRIMARY KEY (`id_equipo`);

--
-- Indices de la tabla `gestion_almacenes`
--
ALTER TABLE `gestion_almacenes`
  ADD PRIMARY KEY (`id_gestion`),
  ADD KEY `gestion_almacenes_FK` (`id_sucursal`);

--
-- Indices de la tabla `ideas_mejora`
--
ALTER TABLE `ideas_mejora`
  ADD PRIMARY KEY (`id_mejora`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_inventario`),
  ADD KEY `inventario_FK` (`id_producto`),
  ADD KEY `inventario_FK_1` (`id_categoria`);

--
-- Indices de la tabla `mantenimiento_equipo`
--
ALTER TABLE `mantenimiento_equipo`
  ADD PRIMARY KEY (`id_mantenimiento`),
  ADD KEY `mantenimiento_equipo_FK` (`id_equipo`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`Id_producto`),
  ADD KEY `producto_FK` (`id_categoria`),
  ADD KEY `producto_FK_1` (`id_proveedor`);

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
-- Indices de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  ADD PRIMARY KEY (`id_sucursal`);

--
-- Indices de la tabla `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id_ticket`);

--
-- Indices de la tabla `transportistas`
--
ALTER TABLE `transportistas`
  ADD PRIMARY KEY (`id_transportista`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `documentacion`
--
ALTER TABLE `documentacion`
  MODIFY `id_documento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `encuestas`
--
ALTER TABLE `encuestas`
  MODIFY `id_encuesta` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `equipo`
--
ALTER TABLE `equipo`
  MODIFY `id_equipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3031;

--
-- AUTO_INCREMENT de la tabla `gestion_almacenes`
--
ALTER TABLE `gestion_almacenes`
  MODIFY `id_gestion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `ideas_mejora`
--
ALTER TABLE `ideas_mejora`
  MODIFY `id_mejora` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_inventario` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `mantenimiento_equipo`
--
ALTER TABLE `mantenimiento_equipo`
  MODIFY `id_mantenimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `Id_producto` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `promociones_y_descuentos`
--
ALTER TABLE `promociones_y_descuentos`
  MODIFY `id_promocion` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  MODIFY `id_sucursal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `ticket`
--
ALTER TABLE `ticket`
  MODIFY `id_ticket` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `transportistas`
--
ALTER TABLE `transportistas`
  MODIFY `id_transportista` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `documentacion`
--
ALTER TABLE `documentacion`
  ADD CONSTRAINT `documentacion_FK` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON UPDATE CASCADE,
  ADD CONSTRAINT `documentacion_FK_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON UPDATE CASCADE,
  ADD CONSTRAINT `documentacion_FK_2` FOREIGN KEY (`id_gestion`) REFERENCES `gestion_almacenes` (`id_gestion`) ON UPDATE CASCADE,
  ADD CONSTRAINT `documentacion_FK_3` FOREIGN KEY (`id_mantenimiento`) REFERENCES `mantenimiento_equipo` (`id_mantenimiento`) ON UPDATE CASCADE,
  ADD CONSTRAINT `documentacion_FK_4` FOREIGN KEY (`id_mejora`) REFERENCES `ideas_mejora` (`id_mejora`) ON UPDATE CASCADE,
  ADD CONSTRAINT `documentacion_FK_5` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `encuestas`
--
ALTER TABLE `encuestas`
  ADD CONSTRAINT `encuestas_FK` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `encuestas_FK_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `gestion_almacenes`
--
ALTER TABLE `gestion_almacenes`
  ADD CONSTRAINT `gestion_almacenes_FK` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursales` (`id_sucursal`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_FK` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`Id_producto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `inventario_FK_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `mantenimiento_equipo`
--
ALTER TABLE `mantenimiento_equipo`
  ADD CONSTRAINT `mantenimiento_equipo_FK` FOREIGN KEY (`id_equipo`) REFERENCES `equipo` (`id_equipo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_FK` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `producto_FK_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
