-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-08-2024 a las 04:17:10
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
-- Estructura de tabla para la tabla `almacenes`
--

CREATE TABLE `almacenes` (
  `id_almacenes` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `id_sucursal` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `almacenes`
--

INSERT INTO `almacenes` (`id_almacenes`, `nombre`, `direccion`, `id_sucursal`) VALUES
(4, 'Almacen A', 'Tegucigalpa', 2),
(5, 'Almacen Central', 'Tegucigalpa', 1),
(6, 'Almacen B', 'Tegucigalpa', 3);

--
-- Disparadores `almacenes`
--
DELIMITER $$
CREATE TRIGGER `after_delete_almacenes` BEFORE DELETE ON `almacenes` FOR EACH ROW BEGIN
    INSERT INTO historicos_almacenes (id_almacenes, acciones, fecha, descripcion)
    VALUES (OLD.id_almacenes, 'Eliminación', NOW(), CONCAT('Se ha eliminado el almacén con ID ', OLD.id_almacenes));
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_insert_almacenes` AFTER INSERT ON `almacenes` FOR EACH ROW BEGIN
    INSERT INTO historicos_almacenes (id_almacenes, acciones, fecha, descripcion)
    VALUES (NEW.id_almacenes, 'Inserción', NOW(), CONCAT('Se ha añadido el almacén con ID ', NEW.id_almacenes));
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_update_almacenes` AFTER UPDATE ON `almacenes` FOR EACH ROW BEGIN
    INSERT INTO historicos_almacenes (id_almacenes, acciones, fecha, descripcion)
    VALUES (NEW.id_almacenes, 'Actualización', NOW(), CONCAT('Se ha actualizado el almacén con ID ', NEW.id_almacenes, ': nombre cambiado a "', NEW.nombre, '" y dirección cambiada a "', NEW.direccion, '".'));
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `capacitacion`
--

CREATE TABLE `capacitacion` (
  `id_capacitacion` int(11) NOT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `tema` varchar(100) DEFAULT NULL,
  `fecha_capacitacion` datetime DEFAULT NULL,
  `duracion` int(11) DEFAULT NULL,
  `resultado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre_categoria` varchar(20) NOT NULL,
  `Descripcion` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre_categoria`, `Descripcion`) VALUES
(1, 'Cocina', 'Electrodomésticos y utensilios para la c'),
(2, 'Lavado y Secado', 'Electrodomésticos para el lavado y secad'),
(3, 'Climatización', 'Aparatos para la regulación de temperatu'),
(4, 'Pequeños Electrodomé', 'Pequeños aparatos para tareas culinarias'),
(5, 'Limpieza', 'Electrodomésticos y accesorios para la l'),
(6, 'Audio y Video', 'Sistemas de entretenimiento de audio y v'),
(7, 'Cuidado Personal', 'Aparatos para el cuidado y bienestar per'),
(8, 'Accesorios y Repuest', 'Accesorios y repuestos para electrodomés');

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
  `documento` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre`, `apellido`, `fecha_nacimiento`, `email`, `telefono`, `direccion`, `fecha_registro`, `tipo`, `documento`) VALUES
(26, 'joseph', 'joestar', '2004-02-21', 'joseph@gmail.com', '3125-8765', 'col.felon', '2024-08-25', 'DNI', '0801200419878'),
(27, 'Gustavo', 'Hernandez', '1999-08-02', 'Gustavo@gmail.com', '96187469', 'col.miraflores', '2024-08-25', 'DNI', '0801199978687'),
(28, 'Juan', 'Lopez', '1980-04-05', 'juanlopez@gmail.com', '31785944', 'Tegucigalpa', '2024-08-24', 'DNI', '0801198020145'),
(29, 'Richard', 'Hernandez', '1995-05-02', 'Gustavo2@gmail.com', '71354321', 'col.miraflores', '2024-08-25', 'DNI', '0801199598765'),
(30, 'Luis', 'Melgar', '2006-08-27', 'luis@gmail.com', '4165-3456', 'col.miraflores', '2024-08-27', 'RTN', '0801-1999-12345'),
(31, 'Jonathan', 'Levi', '2004-08-27', 'joseph@gmail.com', '7135-4321', 'col.felon', '2024-08-27', 'DNI', '0801199978578');

--
-- Disparadores `cliente`
--
DELIMITER $$
CREATE TRIGGER `after_delete_clientes` BEFORE DELETE ON `cliente` FOR EACH ROW BEGIN
    INSERT INTO historicos_clientes (id_cliente, acciones, fecha, descripcion)
    VALUES (OLD.id_cliente, 'Eliminación', NOW(), CONCAT('Se ha eliminado el cliente con ID ', OLD.id_cliente));
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_insert_clientes` AFTER INSERT ON `cliente` FOR EACH ROW BEGIN
    INSERT INTO historicos_clientes (id_cliente, acciones, fecha, descripcion)
    VALUES (NEW.id_cliente, 'Inserción', NOW(), CONCAT('Se ha añadido el cliente con ID ', NEW.id_cliente));
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_insertar_cliente` AFTER INSERT ON `cliente` FOR EACH ROW BEGIN
    INSERT INTO documentacion_clientes (nombre, apellido, tipo, documento, fecha_nacimiento)
    VALUES (NEW.nombre, NEW.apellido, NEW.tipo, NEW.documento, NEW.fecha_nacimiento);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_update_clientes` AFTER UPDATE ON `cliente` FOR EACH ROW BEGIN
    INSERT INTO historicos_clientes (id_cliente, acciones, fecha, descripcion)
    VALUES (NEW.id_cliente, 'Actualización', NOW(), CONCAT('Se ha actualizado el cliente con ID ', NEW.id_cliente));
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_de_factura`
--

CREATE TABLE `detalles_de_factura` (
  `id_detalle` int(11) NOT NULL,
  `id_factura` int(11) DEFAULT NULL,
  `id_producto` int(100) DEFAULT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `cantidad` varchar(50) DEFAULT NULL,
  `precio_unitario` float DEFAULT NULL,
  `subtotal` decimal(10,0) DEFAULT NULL,
  `total` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_de_compra_cliente`
--

CREATE TABLE `detalle_de_compra_cliente` (
  `id_detalle` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(50) NOT NULL,
  `precio_unitario` decimal(10,0) DEFAULT NULL,
  `subtotal` decimal(10,0) DEFAULT NULL,
  `id_impuesto` int(11) DEFAULT NULL,
  `total` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_de_compra_proveedor`
--

CREATE TABLE `detalle_de_compra_proveedor` (
  `id_detalle` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(50) NOT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `id_impuesto` int(11) DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_de_compra_proveedor`
--

INSERT INTO `detalle_de_compra_proveedor` (`id_detalle`, `id_pedido`, `id_producto`, `cantidad`, `precio_unitario`, `id_impuesto`, `subtotal`, `total`, `id_estado`, `id_empleado`) VALUES
(15, 11, 3, 20, 400.00, 5, 8000.00, 8640.00, NULL, NULL),
(16, 15, 3, 132, 400.00, 4, 52800.00, 62304.00, NULL, NULL),
(17, 16, 2, 10, 200.00, 4, 2000.00, 2200.00, NULL, NULL),
(18, 16, 2, 1, 200.00, 3, 200.00, 220.00, NULL, NULL),
(19, 17, 1, 20, 150.00, 3, 3000.00, 3000.00, NULL, NULL),
(20, 17, 4, 30, 80.00, 5, 2400.00, 2400.00, NULL, NULL),
(21, 18, 10, 100, 350.00, 2, 35000.00, 35000.00, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devoluciones_compras`
--

CREATE TABLE `devoluciones_compras` (
  `id_devolucion` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_detalle` int(11) NOT NULL,
  `fecha_devolucion` date NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `cantidad_devuelta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Disparadores `devoluciones_compras`
--
DELIMITER $$
CREATE TRIGGER `actualizar_inventario_en_devolucion` AFTER INSERT ON `devoluciones_compras` FOR EACH ROW BEGIN
    DECLARE cantidad_en_detalle INT;

    -- Verifica la cantidad en el detalle de compra
    SELECT cantidad INTO cantidad_en_detalle 
    FROM detalle_de_compra_proveedor 
    WHERE id_detalle = NEW.id_detalle;

    -- Verifica que la cantidad devuelta no sea mayor a la cantidad en el detalle
    IF NEW.cantidad_devuelta > cantidad_en_detalle THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No puedes devolver más cantidad de la que se compró.';
    ELSE
        -- Actualiza la cantidad en el inventario
        UPDATE inventario 
        SET cantidad_en_stock = cantidad_en_stock - NEW.cantidad_devuelta
        WHERE id_producto = (SELECT id_producto FROM detalle_de_compra_proveedor WHERE id_detalle = NEW.id_detalle);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devoluciones_ventas`
--

CREATE TABLE `devoluciones_ventas` (
  `id_devolucion` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_detalle` int(11) NOT NULL,
  `fecha_devolucion` date NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `cantidad_devuelta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `devoluciones_ventas`
--

INSERT INTO `devoluciones_ventas` (`id_devolucion`, `id_pedido`, `id_detalle`, `fecha_devolucion`, `motivo`, `cantidad_devuelta`) VALUES
(1, 1, 3, '2024-08-23', 'Equipamiento dañado', 2),
(2, 6, 5, '2024-08-23', 'Daño', 2);

--
-- Disparadores `devoluciones_ventas`
--
DELIMITER $$
CREATE TRIGGER `actualizar_inventario_en_devolucion_compras` AFTER INSERT ON `devoluciones_ventas` FOR EACH ROW BEGIN
    DECLARE cantidad_en_detalle INT;

    -- Verifica la cantidad en el detalle de compra
    SELECT cantidad INTO cantidad_en_detalle
    FROM detalle_de_compra_cliente
    WHERE id_detalle = NEW.id_detalle;

    -- Verifica que la cantidad devuelta no sea mayor a la cantidad en el detalle
    IF NEW.cantidad_devuelta > cantidad_en_detalle THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'No puedes devolver más cantidad de la que se compró.';
    ELSE
        -- Actualiza la cantidad en el inventario sumando la cantidad devuelta
        UPDATE inventario
        SET cantidad_en_stock = cantidad_en_stock + NEW.cantidad_devuelta
        WHERE id_producto = (SELECT id_producto FROM detalle_de_compra_cliente WHERE id_detalle = NEW.id_detalle);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `distribucion_almacenes`
--

CREATE TABLE `distribucion_almacenes` (
  `id_distribucion` int(11) NOT NULL,
  `id_almacenes_origen` int(11) DEFAULT NULL,
  `id_almacenes_destino` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `distribucion_almacenes`
--

INSERT INTO `distribucion_almacenes` (`id_distribucion`, `id_almacenes_origen`, `id_almacenes_destino`, `id_producto`, `cantidad`, `fecha`) VALUES
(29, 4, 5, 37, 2, '2024-08-15'),
(33, 5, 6, 37, 2, '2024-08-18'),
(34, 5, 6, 53, 102, '2024-08-23');

--
-- Disparadores `distribucion_almacenes`
--
DELIMITER $$
CREATE TRIGGER `manejar_distribucion` AFTER INSERT ON `distribucion_almacenes` FOR EACH ROW BEGIN
    DECLARE stock_actual INT;
    DECLARE registro_existente INT;

    -- Verificar si ya existe un registro para el almacén y producto en destino
    SELECT COUNT(*) INTO registro_existente
    FROM inventario_almacenes
    WHERE id_almacenes = NEW.id_almacenes_destino AND id_producto = NEW.id_producto;

    -- Caso 1: Transferencia desde Inventario Central (ID = 5) a un Almacén
    IF NEW.id_almacenes_origen = 5 THEN
        -- Verificar la cantidad en stock en el inventario central
        SELECT cantidad_en_stock INTO stock_actual
        FROM inventario
        WHERE id_producto = NEW.id_producto;

        -- Comprobar si hay suficiente stock en Inventario Central
        IF stock_actual >= NEW.cantidad THEN
            -- Restar la cantidad del inventario central
            UPDATE inventario
            SET cantidad_en_stock = cantidad_en_stock - NEW.cantidad
            WHERE id_producto = NEW.id_producto;

            -- Si el registro ya existe, actualiza la cantidad, si no, inserta un nuevo registro
            IF registro_existente > 0 THEN
                UPDATE inventario_almacenes
                SET cantidad_en_stock = cantidad_en_stock + NEW.cantidad, 
                    fecha_ultima_actualizacion = NOW()
                WHERE id_almacenes = NEW.id_almacenes_destino AND id_producto = NEW.id_producto;
            ELSE
                INSERT INTO inventario_almacenes (id_almacenes, id_producto, cantidad_en_stock, stock_minimo, stock_maximo, fecha_ultima_actualizacion)
                VALUES (NEW.id_almacenes_destino, NEW.id_producto, NEW.cantidad, 0, 1000, NOW());
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'No hay suficiente stock en Inventario Central para realizar la transferencia';
        END IF;

    -- Caso 2: Transferencia desde un Almacén a Inventario Central (ID = 5)
    ELSEIF NEW.id_almacenes_destino = 5 THEN
        -- Verificar la cantidad en stock en el almacén de origen
        SELECT cantidad_en_stock INTO stock_actual
        FROM inventario_almacenes
        WHERE id_almacenes = NEW.id_almacenes_origen AND id_producto = NEW.id_producto;

        -- Comprobar si hay suficiente stock en el almacén de origen
        IF stock_actual >= NEW.cantidad THEN
            -- Restar la cantidad del inventario del almacén de origen
            UPDATE inventario_almacenes
            SET cantidad_en_stock = cantidad_en_stock - NEW.cantidad
            WHERE id_almacenes = NEW.id_almacenes_origen AND id_producto = NEW.id_producto;

            -- Sumar la cantidad al inventario central
            UPDATE inventario
            SET cantidad_en_stock = cantidad_en_stock + NEW.cantidad
            WHERE id_producto = NEW.id_producto;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'No hay suficiente stock en el almacén de origen para realizar la transferencia';
        END IF;

    -- Caso 3: Transferencia entre dos almacenes (excluyendo Inventario Central)
    ELSE
        -- Verificar la cantidad en stock en el almacén de origen
        SELECT cantidad_en_stock INTO stock_actual
        FROM inventario_almacenes
        WHERE id_almacenes = NEW.id_almacenes_origen AND id_producto = NEW.id_producto;

        -- Comprobar si hay suficiente stock en el almacén de origen
        IF stock_actual >= NEW.cantidad THEN
            -- Restar la cantidad del inventario del almacén de origen
            UPDATE inventario_almacenes
            SET cantidad_en_stock = cantidad_en_stock - NEW.cantidad
            WHERE id_almacenes = NEW.id_almacenes_origen AND id_producto = NEW.id_producto;

            -- Si el registro ya existe, actualiza la cantidad, si no, inserta un nuevo registro
            IF registro_existente > 0 THEN
                UPDATE inventario_almacenes
                SET cantidad_en_stock = cantidad_en_stock + NEW.cantidad, 
                    fecha_ultima_actualizacion = NOW()
                WHERE id_almacenes = NEW.id_almacenes_destino AND id_producto = NEW.id_producto;
            ELSE
                INSERT INTO inventario_almacenes (id_almacenes, id_producto, cantidad_en_stock, stock_minimo, stock_maximo, fecha_ultima_actualizacion)
                VALUES (NEW.id_almacenes_destino, NEW.id_producto, NEW.cantidad, 0, 1000, NOW());
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'No hay suficiente stock en el almacén de origen para realizar la transferencia';
        END IF;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documentacion_clientes`
--

CREATE TABLE `documentacion_clientes` (
  `id_documentoc` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `apellido` text NOT NULL,
  `tipo` text NOT NULL,
  `documento` int(16) NOT NULL,
  `fecha_nacimiento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `documentacion_clientes`
--

INSERT INTO `documentacion_clientes` (`id_documentoc`, `nombre`, `apellido`, `tipo`, `documento`, `fecha_nacimiento`) VALUES
(5, 'Dante', 'Valladares', 'DNI ', 2147483647, '2024-08-02'),
(6, 'Gustavo ', 'Hernandez', 'DNI ', 801, '1999-08-02'),
(7, 'Juan', 'Lopez', 'DNI', 2147483647, '1980-04-05'),
(8, 'Richard', 'Hernandez', 'DNI', 2147483647, '1995-05-02'),
(9, 'Luis', 'Melgar', 'RTN', 2147483647, '2006-08-27'),
(10, 'Jonathan', 'Levi', 'DNI', 2147483647, '2004-08-27');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documento_empleado`
--

CREATE TABLE `documento_empleado` (
  `id_documento` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `documento` varchar(14) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `documento_empleado`
--

INSERT INTO `documento_empleado` (`id_documento`, `nombre`, `apellido`, `tipo`, `documento`, `fecha_nacimiento`) VALUES
(1, 'Juan', 'Pérez', 'DNI', '12345678', '1985-04-23'),
(2, 'Ana', 'Gómez', 'Pasaporte', 'A1234567', '1990-06-17'),
(3, 'Carlos', 'López', 'RTN', '123456789', '1982-11-30'),
(4, 'María', 'Torres', 'DNI', '87654321', '1987-09-15'),
(5, 'Luis', 'Fernández', 'Pasaporte', 'B7654321', '1978-03-22'),
(6, 'Carmen', 'Martínez', 'RTN', '234567890', '1995-07-10'),
(7, 'Antonio', 'Sánchez', 'DNI', '34567890', '1983-12-05'),
(8, 'Laura', 'Romero', 'Pasaporte', 'C3456789', '1992-10-25'),
(9, 'Javier', 'Ruiz', 'RTN', '456789012', '1981-05-14'),
(10, 'Isabel', 'Hernández', 'DNI', '56789012', '1993-01-09'),
(11, 'Pedro', 'García', 'Pasaporte', 'D5678901', '1989-08-08'),
(12, 'Sonia', 'Jiménez', 'RTN', '678901234', '1977-04-12'),
(13, 'Diego', 'Gil', 'DNI', '78901234', '1986-06-20'),
(14, 'Elena', 'Ortiz', 'Pasaporte', 'E7890123', '1991-11-18'),
(15, 'Francisco', 'Castillo', 'RTN', '890123456', '1984-02-28'),
(16, 'ivan', 'joestar', 'RTN', '0801-1998-9876', '1995-05-02'),
(18, 'Joshua', 'Martinez', 'RTN', '0801-1998-1988', '1995-05-02'),
(19, 'Dante', 'Valladares', 'RTN', '0801-1998-9852', '1998-03-02'),
(20, 'Prueba', 'Prueba', 'RTN', '0801-2004-1940', '2006-08-27'),
(21, 'Kevin', 'Zamora', 'RTN', '0801-2000-4567', '2000-07-27'),
(22, 'Renato', 'Lizardo', 'RTN', '0801-1999-7845', '1999-10-28'),
(23, 'Kevin', 'Zamora', 'RTN', '0801-1999-1236', '1999-07-27'),
(24, 'Kevin', 'Zamora', 'RTN', '0801-1999-1254', '2001-07-28'),
(25, '.', '.', 'RTN', '0801-1995-2654', '1995-05-05'),
(26, 'Luis', 'Melgar', 'RTN', '0801-1995-5245', '1995-03-05'),
(27, 'melissa', 'oseguera', 'RTN', '0801-2000-1236', '2000-02-08');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(6) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `id_puesto` varchar(50) NOT NULL,
  `fecha_contratacion` date NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `documento` varchar(14) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `nombre`, `apellido`, `fecha_nacimiento`, `id_puesto`, `fecha_contratacion`, `id_sucursal`, `email`, `telefono`, `tipo`, `documento`, `password`) VALUES
(18, 'ivan', 'joestar', '1995-05-02', '3', '2024-08-26', 2, 'ivans@gmail.com', '4789-5875', 'RTN', '0801-1998-9876', '12345678'),
(20, 'Joshua', 'Martinez', '1995-05-02', '10', '2024-08-26', 1, 'joshua@gmail.com', '4165-3456', 'RTN', '0801-1998-1988', 'joshua'),
(21, 'Dante', 'Valladares', '1998-03-02', '4', '2024-08-27', 3, 'dante@gmail.com', '33658978', 'RTN', '0801-1998-9852', 'Dante123'),
(24, 'Renato', 'Lizardo', '1999-10-28', '3', '2024-08-27', 4, 'renato@gmail.com', '33458796', 'RTN', '0801-1999-7845', 'Renato123'),
(26, 'Kevin', 'Zamora', '2001-07-28', '3', '2024-08-27', 6, 'kevin@gmail.com', '33225564', 'RTN', '0801-1999-1254', '12345'),
(28, 'Luis', 'Melgar', '1995-03-05', '3', '2024-08-27', 5, 'luis@gmail.com', '33658574', 'RTN', '0801-1995-5245', 'luis123'),
(29, 'melissa', 'oseguera', '2000-02-08', '3', '2024-08-28', 2, 'melissa@gmail.com', '98586352', 'RTN', '0801-2000-1236', 'melissa123');

--
-- Disparadores `empleados`
--
DELIMITER $$
CREATE TRIGGER `after_empleado_insert` AFTER INSERT ON `empleados` FOR EACH ROW BEGIN
    INSERT INTO historicos_empleados (
        id_empleado, 
        acciones, 
        fecha, 
        descripcion
    ) VALUES (
        NEW.id_empleado, 
        'Insertar', 
        NOW(), 
        CONCAT('Se ha insertado el empleado: ', NEW.nombre, ' ', NEW.apellido, 
               ' con puesto: ', NEW.id_puesto, 
               ', fecha de nacimiento: ', NEW.fecha_nacimiento, 
               ', sucursal: ', NEW.id_sucursal, 
               ', email: ', NEW.email, 
               ', teléfono: ', NEW.telefono, 
               ', tipo: ', NEW.tipo, 
               ', documento: ', NEW.documento)
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_empleado_update` AFTER UPDATE ON `empleados` FOR EACH ROW BEGIN
    INSERT INTO historicos_empleados (
        id_empleado, 
        acciones, 
        fecha, 
        descripcion
    ) VALUES (
        NEW.id_empleado, 
        'Actualizar', 
        NOW(), 
        CONCAT('Se ha actualizado el empleado: ', OLD.nombre, ' ', OLD.apellido, 
               ' de puesto: ', OLD.id_puesto, 
               ' a: ', NEW.id_puesto, 
               ', de fecha de nacimiento: ', OLD.fecha_nacimiento, 
               ' a: ', NEW.fecha_nacimiento, 
               ', en sucursal: ', OLD.id_sucursal, 
               ' a: ', NEW.id_sucursal, 
               ', email: ', OLD.email, 
               ' a: ', NEW.email, 
               ', teléfono: ', OLD.telefono, 
               ' a: ', NEW.telefono, 
               ', tipo: ', OLD.tipo, 
               ' a: ', NEW.tipo, 
               ', documento: ', OLD.documento, 
               ' a: ', NEW.documento)
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_empleados_insert` AFTER INSERT ON `empleados` FOR EACH ROW BEGIN
    INSERT INTO usuarios (
        id_usuario,
        primer_nombre,
        primer_apellido,
        correo,
        password,
        super_usuario,
        usuario_activo,
        id_sucursal
    )
    VALUES (
        NEW.id_empleado,
        NEW.nombre,
        NEW.apellido,
        NEW.email,
        NEW.password,
        0, -- super_usuario
        1, -- usuario_activo
        NEW.id_sucursal
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_employee_insert` AFTER INSERT ON `empleados` FOR EACH ROW BEGIN
    INSERT INTO documento_empleado (nombre, apellido, tipo, documento, fecha_nacimiento)
    VALUES (NEW.nombre, NEW.apellido, NEW.tipo, NEW.documento, NEW.fecha_nacimiento);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `before_delete_empleado` BEFORE DELETE ON `empleados` FOR EACH ROW BEGIN
    INSERT INTO historicos_empleados (
        id_empleado, 
        acciones, 
        fecha, 
        descripcion
    ) VALUES (
        OLD.id_empleado, 
        'Eliminar', 
        NOW(), 
        CONCAT('Se ha eliminado el empleado: ', OLD.nombre, ' ', OLD.apellido, 
               ' con puesto: ', OLD.id_puesto, 
               ', fecha de nacimiento: ', OLD.fecha_nacimiento, 
               ', sucursal: ', OLD.id_sucursal, 
               ', email: ', OLD.email, 
               ', teléfono: ', OLD.telefono, 
               ', tipo: ', OLD.tipo, 
               ', documento: ', OLD.documento)
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `delete_usuario_after_empleado` AFTER DELETE ON `empleados` FOR EACH ROW BEGIN
    DELETE FROM usuarios
    WHERE id_usuario = OLD.id_empleado;
END
$$
DELIMITER ;

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
(3, 'Router', 'TP-Link Ar', 'SN1122334455', 'Activo'),
(4, 'Monitor', 'Samsung S2', 'SN2233445566', 'Inactivo'),
(5, 'Teclado', 'Logitech K', 'SN3344556677', 'Activo'),
(6, 'Mouse', 'Logitech M', 'SN4455667788', 'Activo'),
(8, 'Cámara', 'Canon EOS ', 'SN6677889900', 'Activo'),
(9, 'Tablet', 'iPad Air', 'SN7788990011', 'Activo'),
(10, 'Switch', 'Cisco SG30', 'SN8899001122', 'Inactivo'),
(11, 'Disco Duro', 'Seagate Ba', 'SN9900112233', 'Activo'),
(12, 'Laptop', 'MacBook Pr', 'SN1011122334', 'Activo'),
(13, 'Smartphone', 'iPhone 12', 'SN1213141516', 'Inactivo'),
(14, 'Altavoz', 'JBL Flip 4', 'SN1415161718', 'Activo'),
(15, 'Consola', 'PS5', 'SN1617181920', 'Activo'),
(3030, 'mecanico', 'nuevo', '3659', 'bueno');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado`
--

CREATE TABLE `estado` (
  `id_estado` int(11) NOT NULL,
  `nombre_estado` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estado`
--

INSERT INTO `estado` (`id_estado`, `nombre_estado`) VALUES
(1, 'En Proceso'),
(2, 'Recibido'),
(3, 'Rechazado'),
(4, 'Cancelado'),
(5, 'Vendido');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factu`
--

CREATE TABLE `factu` (
  `id_factura` int(100) NOT NULL,
  `id_sar` int(100) NOT NULL,
  `numero_factura` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `factu`
--

INSERT INTO `factu` (`id_factura`, `id_sar`, `numero_factura`) VALUES
(13, 18, '001-150-00-00000150'),
(14, 19, '002-255-00-00000255'),
(16, 21, '004-661-99-45134661'),
(17, 22, '003-000-00-00000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `id_factura` int(11) NOT NULL,
  `id_sar` int(11) DEFAULT NULL,
  `total` decimal(10,0) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `documento` varchar(100) DEFAULT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` int(11) DEFAULT NULL,
  `subtotal` varchar(100) DEFAULT NULL,
  `id_impuesto` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `garantia`
--

CREATE TABLE `garantia` (
  `id_garantia` int(11) NOT NULL,
  `duracion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `garantia`
--

INSERT INTO `garantia` (`id_garantia`, `duracion`) VALUES
(1, '1 Semana'),
(2, '1 mes'),
(3, '6 meses'),
(4, '1 años'),
(5, '5 años');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_de_pagos`
--

CREATE TABLE `historial_de_pagos` (
  `id_pago` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_factura` int(11) DEFAULT NULL,
  `fecha_pago` datetime DEFAULT NULL,
  `monto` decimal(10,0) DEFAULT NULL,
  `id_metodo` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historicos_almacenes`
--

CREATE TABLE `historicos_almacenes` (
  `id_historicos` int(11) NOT NULL,
  `id_almacenes` int(11) DEFAULT NULL,
  `acciones` varchar(100) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `descripcion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historicos_almacenes`
--

INSERT INTO `historicos_almacenes` (`id_historicos`, `id_almacenes`, `acciones`, `fecha`, `descripcion`) VALUES
(1, NULL, 'Inserción', '2024-08-02 16:23:40', 'Se ha añadido el almacén con ID 2'),
(2, NULL, 'Actualización', '2024-08-02 16:30:32', 'Se ha actualizado el almacén con ID 2: nombre cambiado a \"Almacén Principal\" y dirección cambiada a '),
(3, NULL, 'Eliminación', '2024-08-02 16:31:34', 'Se ha eliminado el almacén con ID 2'),
(4, NULL, 'Inserción', '2024-08-03 02:55:50', 'Se ha añadido el almacén con ID 3'),
(5, NULL, 'Actualización', '2024-08-03 02:56:34', 'Se ha actualizado el almacén con ID 3: nombre cambiado a \"Almacem\" y dirección cambiada a \"Cortes\".'),
(6, NULL, 'Eliminación', '2024-08-03 04:27:46', 'Se ha eliminado el almacén con ID 3'),
(8, NULL, 'Eliminación', '2024-08-13 22:22:28', 'Se ha eliminado el almacén con ID 1'),
(9, 4, 'Inserción', '2024-08-14 00:40:42', 'Se ha añadido el almacén con ID 4'),
(10, 5, 'Inserción', '2024-08-14 01:13:50', 'Se ha añadido el almacén con ID 5'),
(11, 4, 'Actualización', '2024-08-14 01:14:00', 'Se ha actualizado el almacén con ID 4: nombre cambiado a \"AlmacenA\" y dirección cambiada a \"Teguciga'),
(12, 6, 'Inserción', '2024-08-14 01:14:18', 'Se ha añadido el almacén con ID 6'),
(13, 4, 'Actualización', '2024-08-14 01:14:25', 'Se ha actualizado el almacén con ID 4: nombre cambiado a \"Almacen A\" y dirección cambiada a \"Tegucig'),
(14, NULL, 'Inserción', '2024-08-23 03:02:16', 'Se ha añadido el almacén con ID 7'),
(15, NULL, 'Actualización', '2024-08-23 03:02:27', 'Se ha actualizado el almacén con ID 7: nombre cambiado a \"Davidse\" y dirección cambiada a \"Colon\".'),
(16, NULL, 'Eliminación', '2024-08-23 04:30:08', 'Se ha eliminado el almacén con ID 7');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historicos_clientes`
--

CREATE TABLE `historicos_clientes` (
  `id_historico` int(11) NOT NULL,
  `acciones` varchar(100) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `descripcion` varchar(100) DEFAULT NULL,
  `id_cliente` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historicos_clientes`
--

INSERT INTO `historicos_clientes` (`id_historico`, `acciones`, `fecha`, `descripcion`, `id_cliente`) VALUES
(1, 'Inserción', '2024-08-03 00:41:57', 'Se ha añadido el cliente con ID 26', 26),
(2, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 1', NULL),
(3, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 2', NULL),
(4, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 3', NULL),
(5, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 4', NULL),
(6, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 5', NULL),
(7, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 6', NULL),
(8, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 7', NULL),
(9, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 8', NULL),
(10, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 9', NULL),
(11, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 10', NULL),
(12, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 11', NULL),
(13, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 12', NULL),
(14, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 13', NULL),
(15, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 14', NULL),
(16, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 15', NULL),
(17, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 16', NULL),
(18, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 17', NULL),
(19, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 18', NULL),
(20, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 19', NULL),
(21, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 20', NULL),
(22, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 21', NULL),
(23, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 22', NULL),
(24, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 23', NULL),
(25, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 24', NULL),
(26, 'Eliminación', '2024-08-03 02:09:28', 'Se ha eliminado el cliente con ID 25', NULL),
(27, 'Inserción', '2024-08-03 13:29:45', 'Se ha añadido el cliente con ID 27', 27),
(28, 'Inserción', '2024-08-24 22:02:30', 'Se ha añadido el cliente con ID 28', 28),
(29, 'Actualización', '2024-08-25 15:00:29', 'Se ha actualizado el cliente con ID 27', 27),
(30, 'Actualización', '2024-08-25 15:00:39', 'Se ha actualizado el cliente con ID 26', 26),
(31, 'Inserción', '2024-08-25 15:02:37', 'Se ha añadido el cliente con ID 29', 29),
(32, 'Actualización', '2024-08-25 15:03:56', 'Se ha actualizado el cliente con ID 26', 26),
(33, 'Actualización', '2024-08-25 15:04:28', 'Se ha actualizado el cliente con ID 27', 27),
(34, 'Inserción', '2024-08-27 18:55:16', 'Se ha añadido el cliente con ID 30', 30),
(35, 'Actualización', '2024-08-27 18:59:37', 'Se ha actualizado el cliente con ID 30', 30),
(36, 'Actualización', '2024-08-27 19:02:45', 'Se ha actualizado el cliente con ID 30', 30),
(37, 'Actualización', '2024-08-27 19:11:15', 'Se ha actualizado el cliente con ID 30', 30),
(38, 'Inserción', '2024-08-27 19:15:36', 'Se ha añadido el cliente con ID 31', 31);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historicos_devolucion`
--

CREATE TABLE `historicos_devolucion` (
  `id_historico` int(11) NOT NULL,
  `id_devolucion` int(11) DEFAULT NULL,
  `acciones` varchar(100) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `descripcion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historicos_empleados`
--

CREATE TABLE `historicos_empleados` (
  `id_historico` int(11) NOT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `acciones` varchar(100) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `descripcion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historicos_empleados`
--

INSERT INTO `historicos_empleados` (`id_historico`, `id_empleado`, `acciones`, `fecha`, `descripcion`) VALUES
(3, NULL, 'INSERT', '2024-08-01 03:23:09', 'Empleado insertado'),
(4, NULL, 'UPDATE', '2024-08-01 03:23:34', 'Empleado actualizado'),
(5, NULL, 'Eliminar', '2024-08-01 16:18:27', 'Empleado eliminado'),
(6, NULL, 'Eliminar', '2024-08-01 17:30:46', 'Se ha eliminado el empleado: Juan Carlos Pérez con puesto: Supervisor, fecha de nacimiento: 1990-06-'),
(7, 1, 'Eliminar', '2024-08-26 17:48:43', 'Se ha eliminado el empleado: José Ramírez con puesto: Gerente, fecha de nacimiento: 1980-01-15, sucu'),
(8, 2, 'Eliminar', '2024-08-26 17:48:43', 'Se ha eliminado el empleado: Laura Martínez con puesto: Vendedora, fecha de nacimiento: 1985-06-20, '),
(9, 3, 'Eliminar', '2024-08-26 17:48:43', 'Se ha eliminado el empleado: Carlos López con puesto: Cajero, fecha de nacimiento: 1990-09-12, sucur'),
(10, 4, 'Eliminar', '2024-08-26 17:48:43', 'Se ha eliminado el empleado: Ana García con puesto: Jefa de almacén, fecha de nacimiento: 1988-03-05'),
(11, 5, 'Eliminar', '2024-08-26 17:48:43', 'Se ha eliminado el empleado: Juan Torres con puesto: Supervisor, fecha de nacimiento: 1992-11-25, su'),
(12, 6, 'Eliminar', '2024-08-26 17:48:43', 'Se ha eliminado el empleado: Marta Gómez con puesto: Recepcionista, fecha de nacimiento: 1985-08-30,'),
(13, 7, 'Eliminar', '2024-08-26 17:48:43', 'Se ha eliminado el empleado: Pedro Fernández con puesto: Contador, fecha de nacimiento: 1991-07-14, '),
(14, 8, 'Eliminar', '2024-08-26 17:48:44', 'Se ha eliminado el empleado: Lucía Díaz con puesto: Administradora, fecha de nacimiento: 1982-04-20,'),
(15, 9, 'Eliminar', '2024-08-26 17:48:44', 'Se ha eliminado el empleado: Jorge Morales con puesto: Analista, fecha de nacimiento: 1993-10-18, su'),
(16, 11, 'Eliminar', '2024-08-26 17:48:44', 'Se ha eliminado el empleado: Andrés Vega con puesto: Ingeniero, fecha de nacimiento: 1994-05-05, suc'),
(17, 12, 'Eliminar', '2024-08-26 17:48:44', 'Se ha eliminado el empleado: Laura Navarro con puesto: Diseñadora, fecha de nacimiento: 1989-09-09, '),
(18, 13, 'Eliminar', '2024-08-26 17:48:44', 'Se ha eliminado el empleado: Rafael Hernández con puesto: Técnico, fecha de nacimiento: 1986-06-22, '),
(19, 14, 'Eliminar', '2024-08-26 17:48:44', 'Se ha eliminado el empleado: Sofía Castillo con puesto: Programadora, fecha de nacimiento: 1995-01-1'),
(20, 18, 'Insertar', '2024-08-26 17:59:11', 'Se ha insertado el empleado: ivan joestar con puesto: 3, fecha de nacimiento: 1995-05-02, sucursal: '),
(21, 18, 'Actualizar', '2024-08-26 18:31:31', 'Se ha actualizado el empleado: ivan joestar de puesto: 3 a: 3, de fecha de nacimiento: 1995-05-02 a:'),
(22, 18, 'Actualizar', '2024-08-26 18:31:36', 'Se ha actualizado el empleado: ivan joestar de puesto: 3 a: 3, de fecha de nacimiento: 1995-05-02 a:'),
(23, 18, 'Actualizar', '2024-08-26 18:31:40', 'Se ha actualizado el empleado: ivan joestar de puesto: 3 a: 3, de fecha de nacimiento: 1995-05-02 a:'),
(24, 20, 'Insertar', '2024-08-26 18:42:22', 'Se ha insertado el empleado: Joshua Martinez con puesto: 10, fecha de nacimiento: 1995-05-02, sucurs'),
(25, 18, 'Actualizar', '2024-08-26 18:43:00', 'Se ha actualizado el empleado: ivan joestar de puesto: 3 a: 3, de fecha de nacimiento: 1995-05-02 a:'),
(26, 21, 'Insertar', '2024-08-27 02:50:13', 'Se ha insertado el empleado: Dante Valladares con puesto: 4, fecha de nacimiento: 1998-03-02, sucurs'),
(27, 20, 'Actualizar', '2024-08-27 03:03:17', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(28, 20, 'Actualizar', '2024-08-27 03:03:42', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(29, 20, 'Actualizar', '2024-08-27 03:04:18', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(30, 20, 'Actualizar', '2024-08-27 03:04:32', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(31, 20, 'Actualizar', '2024-08-27 03:04:52', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(32, 20, 'Actualizar', '2024-08-27 03:15:41', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(33, 20, 'Actualizar', '2024-08-27 03:15:46', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(34, 20, 'Actualizar', '2024-08-27 03:15:51', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(35, 22, 'Insertar', '2024-08-27 03:20:19', 'Se ha insertado el empleado: Prueba Prueba con puesto: 5, fecha de nacimiento: 2006-08-27, sucursal:'),
(36, 20, 'Actualizar', '2024-08-27 07:39:11', 'Se ha actualizado el empleado: Joshua Martinez de puesto: 10 a: 10, de fecha de nacimiento: 1995-05-'),
(37, 23, 'Insertar', '2024-08-27 08:36:50', 'Se ha insertado el empleado: Kevin Zamora con puesto: 3, fecha de nacimiento: 2000-07-27, sucursal: '),
(38, 24, 'Insertar', '2024-08-27 10:13:37', 'Se ha insertado el empleado: Renato Lizardo con puesto: 3, fecha de nacimiento: 1999-10-28, sucursal'),
(39, 22, 'Eliminar', '2024-08-27 10:48:25', 'Se ha eliminado el empleado: Prueba Prueba con puesto: 5, fecha de nacimiento: 2006-08-27, sucursal:'),
(40, 23, 'Eliminar', '2024-08-27 10:48:25', 'Se ha eliminado el empleado: Kevin Zamora con puesto: 3, fecha de nacimiento: 2000-07-27, sucursal: '),
(41, 25, 'Insertar', '2024-08-27 12:23:42', 'Se ha insertado el empleado: Kevin Zamora con puesto: 3, fecha de nacimiento: 1999-07-27, sucursal: '),
(42, 25, 'Eliminar', '2024-08-27 12:29:12', 'Se ha eliminado el empleado: Kevin Zamora con puesto: 3, fecha de nacimiento: 1999-07-27, sucursal: '),
(43, 26, 'Insertar', '2024-08-27 12:36:07', 'Se ha insertado el empleado: Kevin Zamora con puesto: 3, fecha de nacimiento: 2001-07-28, sucursal: '),
(44, 27, 'Insertar', '2024-08-27 23:11:11', 'Se ha insertado el empleado: . . con puesto: 3, fecha de nacimiento: 1995-05-05, sucursal: 5, email:'),
(45, 27, 'Eliminar', '2024-08-27 23:11:39', 'Se ha eliminado el empleado: . . con puesto: 3, fecha de nacimiento: 1995-05-05, sucursal: 5, email:'),
(46, 28, 'Insertar', '2024-08-27 23:12:35', 'Se ha insertado el empleado: Luis Melgar con puesto: 3, fecha de nacimiento: 1995-03-05, sucursal: 5'),
(47, 29, 'Insertar', '2024-08-28 00:46:19', 'Se ha insertado el empleado: melissa oseguera con puesto: 3, fecha de nacimiento: 2000-02-08, sucurs');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historicos_impuestos`
--

CREATE TABLE `historicos_impuestos` (
  `id_historico` int(11) NOT NULL,
  `id_impuesto` int(11) DEFAULT NULL,
  `acciones` varchar(100) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `descripcion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historicos_impuestos`
--

INSERT INTO `historicos_impuestos` (`id_historico`, `id_impuesto`, `acciones`, `fecha`, `descripcion`) VALUES
(1, NULL, 'Insertar', '2024-08-01 03:48:14', 'Se ha insertado un impuesto: IVA con tasa: 0.15'),
(2, NULL, 'Actualizar', '2024-08-01 03:48:45', 'Se ha actualizado el impuesto: IVA Modificado de tasa: 0.15 a: 0.18'),
(4, NULL, 'Eliminar', '2024-08-01 03:50:05', 'Se ha eliminado el impuesto: IVA Modificado con tasa: 0.18'),
(5, NULL, 'Insertar', '2024-08-03 01:09:30', 'Se ha insertado un impuesto: IVA con tasa: 15.00'),
(6, NULL, 'Insertar', '2024-08-03 01:09:30', 'Se ha insertado un impuesto: ISR con tasa: 25.00'),
(7, NULL, 'Insertar', '2024-08-03 01:09:30', 'Se ha insertado un impuesto: ISV con tasa: 12.00'),
(8, 5, 'Insertar', '2024-08-03 02:30:24', 'Se ha insertado un impuesto: ISV con tasa: 0.18'),
(9, NULL, 'Eliminar', '2024-08-03 02:30:39', 'Se ha eliminado el impuesto: ISV con tasa: 12.00'),
(10, NULL, 'Eliminar', '2024-08-03 02:30:42', 'Se ha eliminado el impuesto: IVA con tasa: 15.00'),
(11, NULL, 'Eliminar', '2024-08-03 02:30:46', 'Se ha eliminado el impuesto: ISR con tasa: 25.00'),
(12, 6, 'Insertar', '2024-08-03 02:30:55', 'Se ha insertado un impuesto: ISV con tasa: 0.15'),
(13, 5, 'Actualizar', '2024-08-03 03:05:29', 'Se ha actualizado el impuesto: ISV de tasa: 0.18 a: 18.00'),
(14, 5, 'Actualizar', '2024-08-03 03:13:29', 'Se ha actualizado el impuesto: ISV de tasa: 18.00 a: 0.18'),
(15, 5, 'Actualizar', '2024-08-08 18:52:57', 'Se ha actualizado el impuesto: ISV de tasa: 0 a: 18'),
(16, 7, 'Insertar', '2024-08-21 16:31:40', 'Se ha insertado un impuesto: ISV con tasa: 12'),
(17, 6, 'Actualizar', '2024-08-23 14:32:17', 'Se ha actualizado el impuesto: Otro de tasa: 0 a: 18'),
(18, 6, 'Actualizar', '2024-08-23 14:33:18', 'Se ha actualizado el impuesto: Excento de tasa: 18 a: 0'),
(19, 8, 'Insertar', '2024-08-23 14:34:12', 'Se ha insertado un impuesto: ISV con tasa: 7'),
(20, 9, 'Insertar', '2024-08-23 14:34:12', 'Se ha insertado un impuesto: ISV con tasa: 5'),
(21, NULL, 'Insertar', '2024-08-23 14:34:56', 'Se ha insertado un impuesto: Prueba con tasa: 16'),
(22, NULL, 'Eliminar', '2024-08-23 14:35:11', 'Se ha eliminado el impuesto: Prueba con tasa: 16'),
(23, 5, 'Eliminar', '2024-08-25 07:47:37', 'Se ha eliminado el impuesto: ISV con tasa: 18'),
(24, 6, 'Eliminar', '2024-08-25 07:47:37', 'Se ha eliminado el impuesto: Excento con tasa: 0'),
(25, 7, 'Eliminar', '2024-08-25 07:47:37', 'Se ha eliminado el impuesto: ISV con tasa: 12'),
(26, 8, 'Eliminar', '2024-08-25 07:47:37', 'Se ha eliminado el impuesto: ISV con tasa: 7'),
(27, 9, 'Eliminar', '2024-08-25 07:47:37', 'Se ha eliminado el impuesto: ISV con tasa: 5'),
(28, 1, 'Insertar', '2024-08-25 07:47:45', 'Se ha insertado un impuesto: Impuesto Exento con tasa: 0'),
(29, 2, 'Insertar', '2024-08-25 07:47:45', 'Se ha insertado un impuesto: Impuesto sobre ventas con tasa: 12'),
(30, 3, 'Insertar', '2024-08-25 07:47:45', 'Se ha insertado un impuesto: Impuesto sobre productos electrónicos con tasa: 10'),
(31, 4, 'Insertar', '2024-08-25 07:47:45', 'Se ha insertado un impuesto: Impuesto sobre artículos de lujo con tasa: 15'),
(32, 5, 'Insertar', '2024-08-25 07:47:45', 'Se ha insertado un impuesto: Impuesto sobre la importación con tasa: 8');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historicos_productos`
--

CREATE TABLE `historicos_productos` (
  `id_historico` int(11) NOT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `accion` varchar(255) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historicos_productos`
--

INSERT INTO `historicos_productos` (`id_historico`, `id_producto`, `accion`, `fecha`, `descripcion`) VALUES
(1, NULL, 'Eliminar', '2024-08-01 03:53:45', 'Se ha eliminado el producto: tacos adidas con precio: 3000.00'),
(2, NULL, 'Actualizar', '2024-08-01 03:54:03', 'Se ha actualizado el producto: pastilla panadol de precio: 5.00 a: 6.00'),
(3, NULL, 'Eliminar', '2024-08-02 02:05:44', 'Se ha eliminado el producto: fallout 4 con precio: 2500.00'),
(4, NULL, 'Insertar', '2024-08-02 14:10:35', 'Se ha insertado el producto: Producto Prueba 2 con precio original: 150.00'),
(8, NULL, 'Insertar', '2024-08-02 15:43:30', 'Se ha insertado el producto: Producto A con precio original: 50.00'),
(9, NULL, 'Insertar', '2024-08-02 15:43:30', 'Se ha insertado el producto: Producto E con precio original: 60.00'),
(10, 37, 'Insertar', '2024-08-03 01:09:49', 'Se ha insertado el producto: Estufa de Gas con precio original: 10000.00'),
(11, 37, 'Actualizar', '2024-08-03 01:09:59', 'Se ha actualizado el producto: Estufa de Gas de precio: 10000.00 a: 10000.00'),
(12, 37, 'Actualizar', '2024-08-03 01:12:21', 'Se ha actualizado el producto: Camisas Polo de precio: 10000.00 a: 200.00'),
(13, 37, 'Actualizar', '2024-08-03 01:12:34', 'Se ha actualizado el producto: Camisas Polo de precio: 200.00 a: 200.00'),
(15, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: crema depiladora con precio: 500.00'),
(16, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: Bad bunny con precio: 350.00'),
(17, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: camisa polo con precio: 600.00'),
(18, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: Reloj con precio: 1500.00'),
(19, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: pantalon con precio: 800.00'),
(20, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: Tennis nike con precio: 2500.00'),
(21, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: pastilla panadol con precio: 6.00'),
(22, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: Computadora dell con precio: 5000.00'),
(23, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: medias  con precio: 200.00'),
(24, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: Producto Prueba 2 con precio: 150.00'),
(25, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: Producto A con precio: 50.00'),
(26, NULL, 'Eliminar', '2024-08-03 03:34:34', 'Se ha eliminado el producto: Producto E con precio: 60.00'),
(27, NULL, 'Insertar', '2024-08-03 03:45:07', 'Se ha insertado el producto: Estufa de Gas con precio original: 10000.00'),
(28, 37, 'Actualizar', '2024-08-03 03:45:37', 'Se ha actualizado el producto: Camisas Polo de precio: 200.00 a: 200.00'),
(29, NULL, 'Eliminar', '2024-08-03 03:58:31', 'Se ha eliminado el producto: Estufa de Gas con precio: 10000.00'),
(30, NULL, 'Insertar', '2024-08-03 06:07:27', 'Se ha insertado el producto: Estufa de Gas con precio original: 10000.00'),
(31, NULL, 'Insertar', '2024-08-03 13:46:57', 'Se ha insertado el producto: Telefono con precio original: 10000.00'),
(32, NULL, 'Insertar', '2024-08-18 15:07:16', 'Se ha insertado el producto: Estufa de Gas con precio original: 2000.00'),
(33, NULL, 'Eliminar', '2024-08-21 16:31:58', 'Se ha eliminado el producto: Estufa de Gas con precio: 10000.00'),
(34, NULL, 'Eliminar', '2024-08-21 16:32:02', 'Se ha eliminado el producto: Telefono con precio: 10000.00'),
(35, NULL, 'Eliminar', '2024-08-21 16:32:05', 'Se ha eliminado el producto: Estufa de Gas con precio: 2000.00'),
(36, 42, 'Insertar', '2024-08-21 16:32:53', 'Se ha insertado el producto: Zambo con precio original: 34.00'),
(37, 47, 'Insertar', '2024-08-21 16:37:52', 'Se ha insertado el producto: Licuadora con precio original: 1200.00'),
(38, 48, 'Insertar', '2024-08-21 16:37:52', 'Se ha insertado el producto: Bicicleta con precio original: 8000.00'),
(39, 49, 'Insertar', '2024-08-21 16:37:52', 'Se ha insertado el producto: Laptop con precio original: 15000.00'),
(40, 50, 'Insertar', '2024-08-21 16:37:52', 'Se ha insertado el producto: Camisa con precio original: 700.00'),
(41, 37, 'Actualizar', '2024-08-21 17:13:21', 'Se ha actualizado el producto: Camisas Polo de precio: 200.00 a: 200.26'),
(42, 51, 'Insertar', '2024-08-23 02:26:15', 'Se ha insertado el producto: Mouse con precio original: 243.00'),
(43, 52, 'Insertar', '2024-08-23 15:48:23', 'Se ha insertado el producto: Mouse Pad con precio original: 150.00'),
(44, 53, 'Insertar', '2024-08-23 15:48:46', 'Se ha insertado el producto: Teclado con precio original: 250.00'),
(45, 1, 'Insertar', '2024-08-23 23:49:25', 'Se ha insertado el producto: Teclado con precio original: 250.00'),
(46, 2, 'Insertar', '2024-08-23 23:49:51', 'Se ha insertado el producto: Mouse con precio original: 125.00'),
(47, 3, 'Insertar', '2024-08-23 23:50:21', 'Se ha insertado el producto: Grapadora con precio original: 75.00'),
(48, 4, 'Insertar', '2024-08-24 01:04:43', 'Se ha insertado el producto: Prueba con precio original: 1166.00'),
(49, 1, 'Insertar', '2024-08-24 03:43:53', 'Se ha insertado el producto: Teclado con precio original: 100.00'),
(50, 2, 'Insertar', '2024-08-24 03:44:15', 'Se ha insertado el producto: Resma de papel con precio original: 25.00'),
(51, 3, 'Insertar', '2024-08-24 03:44:36', 'Se ha insertado el producto: Mouse Pad con precio original: 150.00'),
(52, 1, 'Eliminar', '2024-08-25 07:48:25', 'Se ha eliminado el producto: Teclado con precio: 100.00'),
(53, 2, 'Eliminar', '2024-08-25 07:48:25', 'Se ha eliminado el producto: Resma de papel con precio: 25.00'),
(54, 3, 'Eliminar', '2024-08-25 07:48:25', 'Se ha eliminado el producto: Mouse Pad con precio: 150.00'),
(55, 1, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Estufa de gas con precio original: 150.00'),
(56, 2, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Horno eléctrico con precio original: 200.00'),
(57, 3, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Refrigerador con precio original: 400.00'),
(58, 4, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cafetera con precio original: 80.00'),
(59, 5, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Tostadora con precio original: 60.00'),
(60, 6, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Lavadora automática con precio original: 500.00'),
(61, 7, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Secadora de ropa con precio original: 450.00'),
(62, 8, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Plancha de vapor con precio original: 70.00'),
(63, 9, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Secadora de manos con precio original: 90.00'),
(64, 10, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Aire acondicionado portátil con precio original: 350.00'),
(65, 11, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Calentador de agua con precio original: 180.00'),
(66, 12, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Ventilador de pie con precio original: 100.00'),
(67, 13, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Humidificador con precio original: 120.00'),
(68, 14, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Licuadora de cocina con precio original: 50.00'),
(69, 15, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Batidora con precio original: 75.00'),
(70, 16, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Procesador de alimentos con precio original: 90.00'),
(71, 17, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Picadora de carne con precio original: 110.00'),
(72, 18, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Exprimidor de jugos con precio original: 65.00'),
(73, 19, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Aspiradora con precio original: 130.00'),
(74, 20, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Trapeador con precio original: 25.00'),
(75, 21, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Limpiador de ventanas con precio original: 40.00'),
(76, 22, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Escoba eléctrica con precio original: 80.00'),
(77, 23, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Pulidor de pisos con precio original: 150.00'),
(78, 24, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Televisor LED con precio original: 500.00'),
(79, 25, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Home theater con precio original: 250.00'),
(80, 26, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Reproductor Blu-ray con precio original: 120.00'),
(81, 27, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Sistema de sonido con precio original: 300.00'),
(82, 28, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Radio portátil con precio original: 60.00'),
(83, 29, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Secador de cabello con precio original: 40.00'),
(84, 30, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Plancha de cabello con precio original: 35.00'),
(85, 31, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Afeitadora eléctrica con precio original: 55.00'),
(86, 32, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Depiladora con precio original: 70.00'),
(87, 33, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cepillo eléctrico con precio original: 45.00'),
(88, 34, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cargador de batería con precio original: 20.00'),
(89, 35, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Filtro de aire con precio original: 25.00'),
(90, 36, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Adaptador universal con precio original: 30.00'),
(91, 37, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Batería recargable con precio original: 15.00'),
(92, 38, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cargador de teléfono con precio original: 12.00'),
(93, 39, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Estufa de inducción con precio original: 250.00'),
(94, 40, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Horno de microondas con precio original: 120.00'),
(95, 41, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cafetera de cápsulas con precio original: 90.00'),
(96, 42, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Batidora de mano con precio original: 60.00'),
(97, 43, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Procesador de cocina con precio original: 130.00'),
(98, 44, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Picadora de verduras con precio original: 85.00'),
(99, 45, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Hervidor de agua con precio original: 55.00'),
(100, 46, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Licuadora de mano con precio original: 70.00'),
(101, 47, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Aspiradora de mano con precio original: 90.00'),
(102, 48, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Limpiador a vapor con precio original: 140.00'),
(103, 49, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Barredora con precio original: 120.00'),
(104, 50, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Reproductor de DVD con precio original: 80.00'),
(105, 51, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Proyector de video con precio original: 350.00'),
(106, 52, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Auriculares con precio original: 70.00'),
(107, 53, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Radio reloj con precio original: 45.00'),
(108, 54, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Secador de pelo profesional con precio original: 50.00'),
(109, 55, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cortapelos con precio original: 40.00'),
(110, 56, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Masajeador con precio original: 75.00'),
(111, 57, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Esterilizador de cabello con precio original: 65.00'),
(112, 58, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Limpiador facial con precio original: 30.00'),
(113, 59, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Kit de reparación de electrodomésticos con precio original: 50.00'),
(114, 60, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Baterías de repuesto con precio original: 20.00'),
(115, 61, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Adaptador de corriente con precio original: 25.00'),
(116, 62, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cable HDMI con precio original: 15.00'),
(117, 63, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Hub USB con precio original: 30.00'),
(118, 64, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Licuadora de alta potencia con precio original: 150.00'),
(119, 65, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Horno de convección con precio original: 200.00'),
(120, 66, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Calentador de ambiente con precio original: 90.00'),
(121, 67, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Refrigerador de vino con precio original: 220.00'),
(122, 68, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Aspiradora con filtro HEPA con precio original: 170.00'),
(123, 69, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Plancha vertical con precio original: 80.00'),
(124, 70, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Rociador de aire con precio original: 120.00'),
(125, 71, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Purificador de agua con precio original: 140.00'),
(126, 72, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Freidora de aire con precio original: 100.00'),
(127, 73, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Batidora profesional con precio original: 180.00'),
(128, 74, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Picadora eléctrica con precio original: 95.00'),
(129, 75, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Espumador de leche con precio original: 65.00'),
(130, 76, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cámara de seguridad con precio original: 200.00'),
(131, 77, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cargador solar con precio original: 50.00'),
(132, 78, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Estación meteorológica con precio original: 75.00'),
(133, 79, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Lámpara de escritorio con precio original: 30.00'),
(134, 80, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Reloj despertador con precio original: 25.00'),
(135, 81, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Consola de videojuegos con precio original: 300.00'),
(136, 82, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Ratón ergonómico con precio original: 45.00'),
(137, 83, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Teclado mecánico con precio original: 60.00'),
(138, 84, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Monitor de computadora con precio original: 180.00'),
(139, 85, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Refrigerador compacto con precio original: 140.00'),
(140, 86, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Aspiradora robot con precio original: 250.00'),
(141, 87, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Televisor 4K con precio original: 600.00'),
(142, 88, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Proyector portátil con precio original: 150.00'),
(143, 89, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cámara de acción con precio original: 250.00'),
(144, 90, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Dron con cámara con precio original: 400.00'),
(145, 91, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Escáner de documentos con precio original: 100.00'),
(146, 92, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Papelera inteligente con precio original: 60.00'),
(147, 93, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Cafetera de filtro con precio original: 45.00'),
(148, 94, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Centrífuga de ensaladas con precio original: 30.00'),
(149, 95, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Calentador eléctrico con precio original: 85.00'),
(150, 96, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Secador de zapatos con precio original: 20.00'),
(151, 97, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Termómetro digital con precio original: 15.00'),
(152, 98, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Purgador de aire con precio original: 95.00'),
(153, 99, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Mueble para TV con precio original: 150.00'),
(154, 100, 'Insertar', '2024-08-25 07:48:31', 'Se ha insertado el producto: Sistema de alarmas con precio original: 220.00'),
(155, 1, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Estufa de gas con precio: 150.00'),
(156, 2, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Horno eléctrico con precio: 200.00'),
(157, 3, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Refrigerador con precio: 400.00'),
(158, 4, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Cafetera con precio: 80.00'),
(159, 5, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Tostadora con precio: 60.00'),
(160, 6, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Lavadora automática con precio: 500.00'),
(161, 7, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Secadora de ropa con precio: 450.00'),
(162, 8, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Plancha de vapor con precio: 70.00'),
(163, 9, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Secadora de manos con precio: 90.00'),
(164, 10, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Aire acondicionado portátil con precio: 350.00'),
(165, 11, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Calentador de agua con precio: 180.00'),
(166, 12, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Ventilador de pie con precio: 100.00'),
(167, 13, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Humidificador con precio: 120.00'),
(168, 14, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Licuadora de cocina con precio: 50.00'),
(169, 15, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Batidora con precio: 75.00'),
(170, 16, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Procesador de alimentos con precio: 90.00'),
(171, 17, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Picadora de carne con precio: 110.00'),
(172, 18, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Exprimidor de jugos con precio: 65.00'),
(173, 19, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Aspiradora con precio: 130.00'),
(174, 20, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Trapeador con precio: 25.00'),
(175, 21, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Limpiador de ventanas con precio: 40.00'),
(176, 22, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Escoba eléctrica con precio: 80.00'),
(177, 23, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Pulidor de pisos con precio: 150.00'),
(178, 24, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Televisor LED con precio: 500.00'),
(179, 25, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Home theater con precio: 250.00'),
(180, 26, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Reproductor Blu-ray con precio: 120.00'),
(181, 27, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Sistema de sonido con precio: 300.00'),
(182, 28, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Radio portátil con precio: 60.00'),
(183, 29, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Secador de cabello con precio: 40.00'),
(184, 30, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Plancha de cabello con precio: 35.00'),
(185, 31, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Afeitadora eléctrica con precio: 55.00'),
(186, 32, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Depiladora con precio: 70.00'),
(187, 33, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Cepillo eléctrico con precio: 45.00'),
(188, 34, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Cargador de batería con precio: 20.00'),
(189, 35, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Filtro de aire con precio: 25.00'),
(190, 36, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Adaptador universal con precio: 30.00'),
(191, 37, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Batería recargable con precio: 15.00'),
(192, 38, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Cargador de teléfono con precio: 12.00'),
(193, 39, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Estufa de inducción con precio: 250.00'),
(194, 40, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Horno de microondas con precio: 120.00'),
(195, 41, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Cafetera de cápsulas con precio: 90.00'),
(196, 42, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Batidora de mano con precio: 60.00'),
(197, 43, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Procesador de cocina con precio: 130.00'),
(198, 44, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Picadora de verduras con precio: 85.00'),
(199, 45, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Hervidor de agua con precio: 55.00'),
(200, 46, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Licuadora de mano con precio: 70.00'),
(201, 47, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Aspiradora de mano con precio: 90.00'),
(202, 48, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Limpiador a vapor con precio: 140.00'),
(203, 49, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Barredora con precio: 120.00'),
(204, 50, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Reproductor de DVD con precio: 80.00'),
(205, 51, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Proyector de video con precio: 350.00'),
(206, 52, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Auriculares con precio: 70.00'),
(207, 53, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Radio reloj con precio: 45.00'),
(208, 54, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Secador de pelo profesional con precio: 50.00'),
(209, 55, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Cortapelos con precio: 40.00'),
(210, 56, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Masajeador con precio: 75.00'),
(211, 57, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Esterilizador de cabello con precio: 65.00'),
(212, 58, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Limpiador facial con precio: 30.00'),
(213, 59, 'Eliminar', '2024-08-25 15:41:28', 'Se ha eliminado el producto: Kit de reparación de electrodomésticos con precio: 50.00'),
(214, 60, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Baterías de repuesto con precio: 20.00'),
(215, 61, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Adaptador de corriente con precio: 25.00'),
(216, 62, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Cable HDMI con precio: 15.00'),
(217, 63, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Hub USB con precio: 30.00'),
(218, 64, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Licuadora de alta potencia con precio: 150.00'),
(219, 65, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Horno de convección con precio: 200.00'),
(220, 66, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Calentador de ambiente con precio: 90.00'),
(221, 67, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Refrigerador de vino con precio: 220.00'),
(222, 68, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Aspiradora con filtro HEPA con precio: 170.00'),
(223, 69, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Plancha vertical con precio: 80.00'),
(224, 70, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Rociador de aire con precio: 120.00'),
(225, 71, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Purificador de agua con precio: 140.00'),
(226, 72, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Freidora de aire con precio: 100.00'),
(227, 73, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Batidora profesional con precio: 180.00'),
(228, 74, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Picadora eléctrica con precio: 95.00'),
(229, 75, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Espumador de leche con precio: 65.00'),
(230, 76, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Cámara de seguridad con precio: 200.00'),
(231, 77, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Cargador solar con precio: 50.00'),
(232, 78, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Estación meteorológica con precio: 75.00'),
(233, 79, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Lámpara de escritorio con precio: 30.00'),
(234, 80, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Reloj despertador con precio: 25.00'),
(235, 81, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Consola de videojuegos con precio: 300.00'),
(236, 82, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Ratón ergonómico con precio: 45.00'),
(237, 83, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Teclado mecánico con precio: 60.00'),
(238, 84, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Monitor de computadora con precio: 180.00'),
(239, 85, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Refrigerador compacto con precio: 140.00'),
(240, 86, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Aspiradora robot con precio: 250.00'),
(241, 87, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Televisor 4K con precio: 600.00'),
(242, 88, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Proyector portátil con precio: 150.00'),
(243, 89, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Cámara de acción con precio: 250.00'),
(244, 90, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Dron con cámara con precio: 400.00'),
(245, 91, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Escáner de documentos con precio: 100.00'),
(246, 92, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Papelera inteligente con precio: 60.00'),
(247, 93, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Cafetera de filtro con precio: 45.00'),
(248, 94, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Centrífuga de ensaladas con precio: 30.00'),
(249, 95, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Calentador eléctrico con precio: 85.00'),
(250, 96, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Secador de zapatos con precio: 20.00'),
(251, 97, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Termómetro digital con precio: 15.00'),
(252, 98, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Purgador de aire con precio: 95.00'),
(253, 99, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Mueble para TV con precio: 150.00'),
(254, 100, 'Eliminar', '2024-08-25 15:41:29', 'Se ha eliminado el producto: Sistema de alarmas con precio: 220.00'),
(255, 1, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Estufa de gas con precio original: 150.00'),
(256, 2, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Horno eléctrico con precio original: 200.00'),
(257, 3, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Refrigerador con precio original: 400.00'),
(258, 4, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cafetera con precio original: 80.00'),
(259, 5, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Tostadora con precio original: 60.00'),
(260, 6, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Lavadora automática con precio original: 500.00'),
(261, 7, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de ropa con precio original: 450.00'),
(262, 8, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Plancha de vapor con precio original: 70.00'),
(263, 9, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de manos con precio original: 90.00'),
(264, 10, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Aire acondicionado portátil con precio original: 350.00'),
(265, 11, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Calentador de agua con precio original: 180.00'),
(266, 12, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Ventilador de pie con precio original: 100.00'),
(267, 13, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Humidificador con precio original: 120.00'),
(268, 14, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Licuadora de cocina con precio original: 50.00'),
(269, 15, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Microondas con precio original: 80.00'),
(270, 16, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Procesador de alimentos con precio original: 150.00'),
(271, 17, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Batidora con precio original: 90.00'),
(272, 18, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Aspiradora con precio original: 120.00'),
(273, 19, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Detergente líquido con precio original: 10.00'),
(274, 20, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Mopa con precio original: 30.00'),
(275, 21, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Escoba eléctrica con precio original: 45.00'),
(276, 22, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Televisor 40 pulgadas con precio original: 400.00'),
(277, 23, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Equipo de sonido con precio original: 250.00'),
(278, 24, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Reproductor Blu-ray con precio original: 150.00'),
(279, 25, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Proyector con precio original: 300.00'),
(280, 26, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Maquinilla de afeitar eléctrica con precio original: 60.00'),
(281, 27, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de cabello con precio original: 40.00'),
(282, 28, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cepillo de dientes eléctrico con precio original: 45.00'),
(283, 29, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cortapelos con precio original: 70.00'),
(284, 30, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Filtro de agua con precio original: 25.00'),
(285, 31, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Repuesto para lavadora con precio original: 15.00'),
(286, 32, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Tapa para olla con precio original: 10.00'),
(287, 33, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Batería para control remoto con precio original: 5.00'),
(288, 34, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Estufa de gas con precio original: 150.00'),
(289, 35, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Horno eléctrico con precio original: 200.00'),
(290, 36, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Refrigerador con precio original: 400.00'),
(291, 37, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cafetera con precio original: 80.00'),
(292, 38, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Tostadora con precio original: 60.00'),
(293, 39, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Lavadora automática con precio original: 500.00'),
(294, 40, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de ropa con precio original: 450.00'),
(295, 41, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Plancha de vapor con precio original: 70.00'),
(296, 42, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de manos con precio original: 90.00'),
(297, 43, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Aire acondicionado portátil con precio original: 350.00'),
(298, 44, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Calentador de agua con precio original: 180.00'),
(299, 45, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Ventilador de pie con precio original: 100.00'),
(300, 46, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Humidificador con precio original: 120.00'),
(301, 47, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Licuadora de cocina con precio original: 50.00'),
(302, 48, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Microondas con precio original: 80.00'),
(303, 49, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Procesador de alimentos con precio original: 150.00'),
(304, 50, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Batidora con precio original: 90.00'),
(305, 51, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Aspiradora con precio original: 120.00'),
(306, 52, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Detergente líquido con precio original: 10.00'),
(307, 53, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Mopa con precio original: 30.00'),
(308, 54, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Escoba eléctrica con precio original: 45.00'),
(309, 55, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Televisor 40 pulgadas con precio original: 400.00'),
(310, 56, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Equipo de sonido con precio original: 250.00'),
(311, 57, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Reproductor Blu-ray con precio original: 150.00'),
(312, 58, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Proyector con precio original: 300.00'),
(313, 59, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Maquinilla de afeitar eléctrica con precio original: 60.00'),
(314, 60, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de cabello con precio original: 40.00'),
(315, 61, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cepillo de dientes eléctrico con precio original: 45.00'),
(316, 62, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cortapelos con precio original: 70.00'),
(317, 63, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Filtro de agua con precio original: 25.00'),
(318, 64, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Repuesto para lavadora con precio original: 15.00'),
(319, 65, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Tapa para olla con precio original: 10.00'),
(320, 66, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Batería para control remoto con precio original: 5.00'),
(321, 67, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Estufa de gas con precio original: 150.00'),
(322, 68, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Horno eléctrico con precio original: 200.00'),
(323, 69, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Refrigerador con precio original: 400.00'),
(324, 70, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cafetera con precio original: 80.00'),
(325, 71, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Tostadora con precio original: 60.00'),
(326, 72, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Lavadora automática con precio original: 500.00'),
(327, 73, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de ropa con precio original: 450.00'),
(328, 74, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Plancha de vapor con precio original: 70.00'),
(329, 75, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de manos con precio original: 90.00'),
(330, 76, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Aire acondicionado portátil con precio original: 350.00'),
(331, 77, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Calentador de agua con precio original: 180.00'),
(332, 78, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Ventilador de pie con precio original: 100.00'),
(333, 79, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Humidificador con precio original: 120.00'),
(334, 80, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Licuadora de cocina con precio original: 50.00'),
(335, 81, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Microondas con precio original: 80.00'),
(336, 82, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Procesador de alimentos con precio original: 150.00'),
(337, 83, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Batidora con precio original: 90.00'),
(338, 84, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Aspiradora con precio original: 120.00'),
(339, 85, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Detergente líquido con precio original: 10.00'),
(340, 86, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Mopa con precio original: 30.00'),
(341, 87, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Escoba eléctrica con precio original: 45.00'),
(342, 88, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Televisor 40 pulgadas con precio original: 400.00'),
(343, 89, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Equipo de sonido con precio original: 250.00'),
(344, 90, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Reproductor Blu-ray con precio original: 150.00'),
(345, 91, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Proyector con precio original: 300.00'),
(346, 92, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Maquinilla de afeitar eléctrica con precio original: 60.00'),
(347, 93, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Secadora de cabello con precio original: 40.00'),
(348, 94, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cepillo de dientes eléctrico con precio original: 45.00'),
(349, 95, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cortapelos con precio original: 70.00'),
(350, 96, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Filtro de agua con precio original: 25.00'),
(351, 97, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Repuesto para lavadora con precio original: 15.00'),
(352, 98, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Tapa para olla con precio original: 10.00'),
(353, 99, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Batería para control remoto con precio original: 5.00'),
(354, 100, 'Insertar', '2024-08-25 15:41:37', 'Se ha insertado el producto: Cepillo de dientes manual con precio original: 10.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ideas_mejora`
--

CREATE TABLE `ideas_mejora` (
  `id_mejora` int(7) NOT NULL,
  `documento` varchar(13) NOT NULL,
  `fecha_propuesta` date NOT NULL,
  `descripcion_idea` text NOT NULL,
  `estado` varchar(50) NOT NULL,
  `fecha_implementacion` date NOT NULL,
  `descripcion_implementacion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `impuesto`
--

CREATE TABLE `impuesto` (
  `id_impuesto` int(11) NOT NULL,
  `tipo_impuesto` varchar(40) NOT NULL,
  `tasa_impuesto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `impuesto`
--

INSERT INTO `impuesto` (`id_impuesto`, `tipo_impuesto`, `tasa_impuesto`) VALUES
(1, 'Impuesto Exento', 0),
(2, 'Impuesto sobre ventas', 12),
(3, 'Impuesto sobre productos electrónicos', 10),
(4, 'Impuesto sobre artículos de lujo', 15),
(5, 'Impuesto sobre la importación', 8);

--
-- Disparadores `impuesto`
--
DELIMITER $$
CREATE TRIGGER `after_insert_impuesto` AFTER INSERT ON `impuesto` FOR EACH ROW BEGIN
    INSERT INTO historicos_impuestos (
        id_impuesto, 
        acciones, 
        fecha, 
        descripcion
    ) VALUES (
        NEW.id_impuesto, 
        'Insertar', 
        NOW(), 
        CONCAT('Se ha insertado un impuesto: ', NEW.tipo_impuesto, ' con tasa: ', NEW.tasa_impuesto)
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_update_impuesto` AFTER UPDATE ON `impuesto` FOR EACH ROW BEGIN
    INSERT INTO historicos_impuestos (
        id_impuesto, 
        acciones, 
        fecha, 
        descripcion
    ) VALUES (
        NEW.id_impuesto, 
        'Actualizar', 
        NOW(), 
        CONCAT('Se ha actualizado el impuesto: ', NEW.tipo_impuesto, ' de tasa: ', OLD.tasa_impuesto, ' a: ', NEW.tasa_impuesto)
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `before_delete_impuesto` BEFORE DELETE ON `impuesto` FOR EACH ROW BEGIN
    INSERT INTO historicos_impuestos (
        id_impuesto, 
        acciones, 
        fecha, 
        descripcion
    ) VALUES (
        OLD.id_impuesto, 
        'Eliminar', 
        NOW(), 
        CONCAT('Se ha eliminado el impuesto: ', OLD.tipo_impuesto, ' con tasa: ', OLD.tasa_impuesto)
    );
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_inventario` int(100) NOT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `cantidad_en_stock` int(100) NOT NULL,
  `stock_minimo` int(100) NOT NULL,
  `stock_maximo` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_inventario`, `id_producto`, `id_categoria`, `cantidad_en_stock`, `stock_minimo`, `stock_maximo`) VALUES
(108, 1, 1, 19, 0, 1000),
(109, 2, 1, 3, 0, 1000),
(110, 3, 1, 130, 0, 150),
(111, 4, 1, 30, 0, 1000),
(112, 5, 1, 0, 0, 1000),
(113, 6, 2, 0, 0, 1000),
(114, 7, 2, 0, 0, 1000),
(115, 8, 2, 0, 0, 1000),
(116, 9, 2, 0, 0, 1000),
(117, 10, 3, 100, 0, 1000),
(118, 11, 3, 0, 0, 1000),
(119, 12, 3, 0, 0, 1000),
(120, 13, 3, 0, 0, 1000),
(121, 14, 4, 0, 0, 1000),
(122, 15, 4, 0, 0, 1000),
(123, 16, 4, 0, 0, 1000),
(124, 17, 4, 0, 0, 1000),
(125, 18, 5, 0, 0, 1000),
(126, 19, 5, 0, 0, 1000),
(127, 20, 5, 0, 0, 1000),
(128, 21, 5, 0, 0, 1000),
(129, 22, 6, 0, 0, 1000),
(130, 23, 6, 0, 0, 1000),
(131, 24, 6, 0, 0, 1000),
(132, 25, 6, 0, 0, 1000),
(133, 26, 7, 0, 0, 1000),
(134, 27, 7, 0, 0, 1000),
(135, 28, 7, 0, 0, 1000),
(136, 29, 7, 0, 0, 1000),
(137, 30, 8, 0, 0, 1000),
(138, 31, 8, 0, 0, 1000),
(139, 32, 8, 0, 0, 1000),
(140, 33, 8, 0, 0, 1000),
(141, 34, 1, 0, 0, 1000),
(142, 35, 1, 0, 0, 1000),
(143, 36, 1, 0, 0, 1000),
(144, 37, 1, 0, 0, 1000),
(145, 38, 1, 0, 0, 1000),
(146, 39, 2, 0, 0, 1000),
(147, 40, 2, 0, 0, 1000),
(148, 41, 2, 0, 0, 1000),
(149, 42, 2, 0, 0, 1000),
(150, 43, 3, 0, 0, 1000),
(151, 44, 3, 0, 0, 1000),
(152, 45, 3, 0, 0, 1000),
(153, 46, 3, 0, 0, 1000),
(154, 47, 4, 0, 0, 1000),
(155, 48, 4, 0, 0, 1000),
(156, 49, 4, 0, 0, 1000),
(157, 50, 4, 0, 0, 1000),
(158, 51, 5, 0, 0, 1000),
(159, 52, 5, 0, 0, 1000),
(160, 53, 5, 0, 0, 1000),
(161, 54, 5, 0, 0, 1000),
(162, 55, 6, 0, 0, 1000),
(163, 56, 6, 0, 0, 1000),
(164, 57, 6, 0, 0, 1000),
(165, 58, 6, 0, 0, 1000),
(166, 59, 7, 0, 0, 1000),
(167, 60, 7, 0, 0, 1000),
(168, 61, 7, 0, 0, 1000),
(169, 62, 7, 0, 0, 1000),
(170, 63, 8, 0, 0, 1000),
(171, 64, 8, 0, 0, 1000),
(172, 65, 8, 0, 0, 1000),
(173, 66, 8, 0, 0, 1000),
(174, 67, 1, 0, 0, 1000),
(175, 68, 1, 0, 0, 1000),
(176, 69, 1, 0, 0, 1000),
(177, 70, 1, 0, 0, 1000),
(178, 71, 1, 0, 0, 1000),
(179, 72, 2, 0, 0, 1000),
(180, 73, 2, 0, 0, 1000),
(181, 74, 2, 0, 0, 1000),
(182, 75, 2, 0, 0, 1000),
(183, 76, 3, 0, 0, 1000),
(184, 77, 3, 0, 0, 1000),
(185, 78, 3, 0, 0, 1000),
(186, 79, 3, 0, 0, 1000),
(187, 80, 4, 0, 0, 1000),
(188, 81, 4, 0, 0, 1000),
(189, 82, 4, 0, 0, 1000),
(190, 83, 4, 0, 0, 1000),
(191, 84, 5, 0, 0, 1000),
(192, 85, 5, 0, 0, 1000),
(193, 86, 5, 0, 0, 1000),
(194, 87, 5, 0, 0, 1000),
(195, 88, 6, 0, 0, 1000),
(196, 89, 6, 0, 0, 1000),
(197, 90, 6, 0, 0, 1000),
(198, 91, 6, 0, 0, 1000),
(199, 92, 7, 0, 0, 1000),
(200, 93, 7, 0, 0, 1000),
(201, 94, 7, 0, 0, 1000),
(202, 95, 7, 0, 0, 1000),
(203, 96, 8, 0, 0, 1000),
(204, 97, 8, 0, 0, 1000),
(205, 98, 8, 0, 0, 1000),
(206, 99, 8, 0, 0, 1000),
(207, 100, 7, 0, 0, 1000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_almacenes`
--

CREATE TABLE `inventario_almacenes` (
  `id_inventario_almacenes` int(11) NOT NULL,
  `id_almacenes` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad_en_stock` int(11) DEFAULT NULL,
  `stock_minimo` int(11) DEFAULT NULL,
  `stock_maximo` int(11) DEFAULT NULL,
  `fecha_ultima_actualizacion` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario_almacenes`
--

INSERT INTO `inventario_almacenes` (`id_inventario_almacenes`, `id_almacenes`, `id_producto`, `cantidad_en_stock`, `stock_minimo`, `stock_maximo`, `fecha_ultima_actualizacion`) VALUES
(1, 4, 37, 3, 0, 1000, '2024-08-15'),
(3, 5, 37, 2, 0, 1000, '2024-08-15'),
(6, 6, 37, 2, 0, 1000, '2024-08-18'),
(7, 6, 53, 102, 0, 1000, '2024-08-23');

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
  `documento` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mantenimiento_equipo`
--

INSERT INTO `mantenimiento_equipo` (`id_mantenimiento`, `id_equipo`, `fecha`, `tipo`, `detalles`, `estado`, `documento`) VALUES
(5, 3030, '2024-08-15', 'electrico', 'ocupo cambio de cier', 'medio', '0801567890124');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_de_pago`
--

CREATE TABLE `metodo_de_pago` (
  `id_metodo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `metodo_de_pago`
--

INSERT INTO `metodo_de_pago` (`id_metodo`, `nombre`) VALUES
(1, 'Tarjeta de Credito'),
(2, 'Efectivo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido_de_compra_cliente`
--

CREATE TABLE `pedido_de_compra_cliente` (
  `id_pedido` int(11) NOT NULL,
  `numero_factura` varchar(20) DEFAULT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `fecha_pedido` date DEFAULT NULL,
  `fecha_entrega_estimada` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `id_metodo` int(11) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `id_sucursal` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Disparadores `pedido_de_compra_cliente`
--
DELIMITER $$
CREATE TRIGGER `actualizar_inventario_restar` AFTER UPDATE ON `pedido_de_compra_cliente` FOR EACH ROW BEGIN
    -- Verifica si el estado del pedido ha cambiado a "vendido" (ID 5)
    IF NEW.id_estado = 5 AND OLD.id_estado <> 5 THEN
        -- Disminuye la cantidad en el inventario por cada detalle de compra relacionado
        UPDATE inventario i
        JOIN detalle_de_compra_cliente d
        ON i.id_producto = d.id_producto
        SET i.cantidad_en_stock = i.cantidad_en_stock - d.cantidad
        WHERE d.id_pedido = NEW.id_pedido;
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_incrementar_numero_factura` AFTER INSERT ON `pedido_de_compra_cliente` FOR EACH ROW BEGIN
    DECLARE v_numero_factura VARCHAR(20);
    DECLARE v_incremento INT;

    -- Validar que el id_sucursal de pedido_de_compra_cliente coincida con el de sar
    -- y que el id_sar de sar coincida con el de factu.
    IF EXISTS (
        SELECT 1
        FROM sar s
        JOIN factu f ON s.id_sar = f.id_sar
        WHERE s.id_sucursal = NEW.id_sucursal
    ) THEN
        -- Obtener el número de factura actual
        SELECT numero_factura
        INTO v_numero_factura
        FROM factu f
        JOIN sar s ON f.id_sar = s.id_sar
        WHERE s.id_sucursal = NEW.id_sucursal
        ORDER BY f.id_factura DESC
        LIMIT 1;
        
        -- Incrementar los últimos 8 dígitos del número de factura
        SET v_incremento = CAST(SUBSTRING(v_numero_factura, -8) AS UNSIGNED) + 1;

        -- Actualizar el número de factura en la tabla factu
        UPDATE factu f
        JOIN sar s ON f.id_sar = s.id_sar
        SET f.numero_factura = CONCAT(SUBSTRING(v_numero_factura, 1, LENGTH(v_numero_factura) - 8), LPAD(v_incremento, 8, '0'))
        WHERE s.id_sucursal = NEW.id_sucursal
        ORDER BY f.id_factura DESC
        LIMIT 1;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido_de_compra_proveedor`
--

CREATE TABLE `pedido_de_compra_proveedor` (
  `id_pedido` int(11) NOT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  `numero_factura` varchar(20) DEFAULT NULL,
  `fecha_pedido` date DEFAULT NULL,
  `fecha_entrega_estimada` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `id_metodo` int(11) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido_de_compra_proveedor`
--

INSERT INTO `pedido_de_compra_proveedor` (`id_pedido`, `id_proveedor`, `numero_factura`, `fecha_pedido`, `fecha_entrega_estimada`, `fecha_entrega`, `id_metodo`, `id_estado`, `id_empleado`) VALUES
(10, 1, '432-45-65-643213', '2024-08-27', '2024-09-03', '2024-09-04', 1, 1, 18),
(11, 1, '234-56-21-345432', '2024-08-27', '2024-09-03', '2024-09-04', 1, 2, 26),
(14, 1, 'None', '2024-08-27', '2024-09-03', '2024-09-04', 1, 1, 26),
(15, 1, '546-26-46-56215', '2024-08-27', '2024-09-03', '2024-09-04', 1, 1, 18),
(16, 1, '333-33-33-33333', '2024-08-27', '2024-09-03', '2024-09-04', 1, 1, 26),
(17, 2, '164-12-64-55265', '2024-08-28', '2024-09-04', '2024-09-05', 1, 2, 26),
(18, 5, '465-46-16-45151', '2024-08-28', '2024-09-04', '2024-09-05', 1, 2, 28);

--
-- Disparadores `pedido_de_compra_proveedor`
--
DELIMITER $$
CREATE TRIGGER `actualizar_inventario` AFTER UPDATE ON `pedido_de_compra_proveedor` FOR EACH ROW BEGIN
    -- Verifica si el estado del pedido ha cambiado a "recibido"
    IF NEW.id_estado = 2 AND OLD.id_estado = 1 THEN
        -- Aumenta la cantidad en el inventario por cada detalle de compra
        UPDATE inventario i
        JOIN detalle_de_compra_proveedor d
        ON i.id_producto = d.id_producto
        SET i.cantidad_en_stock = i.cantidad_en_stock + d.cantidad
        WHERE d.id_pedido = NEW.id_pedido;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_producto` int(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  `original_precio` decimal(10,2) DEFAULT NULL,
  `id_impuesto` int(11) DEFAULT NULL,
  `id_promocion` int(100) DEFAULT NULL,
  `id_garantia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_producto`, `nombre`, `id_categoria`, `id_proveedor`, `original_precio`, `id_impuesto`, `id_promocion`, `id_garantia`) VALUES
(1, 'Estufa de gas', 1, 1, 150.00, 2, 11, 4),
(2, 'Horno eléctrico', 1, 2, 200.00, 3, 12, 5),
(3, 'Refrigerador', 1, 2, 400.00, 2, 13, 5),
(4, 'Cafetera', 1, 7, 80.00, 1, 14, 3),
(5, 'Tostadora', 1, 8, 60.00, 2, 15, 2),
(6, 'Lavadora automática', 2, 3, 500.00, 4, 16, 3),
(7, 'Secadora de ropa', 2, 4, 450.00, 2, 15, 2),
(8, 'Plancha de vapor', 2, 7, 70.00, 3, 12, 1),
(9, 'Secadora de manos', 2, 8, 90.00, 1, 11, 4),
(10, 'Aire acondicionado portátil', 3, 5, 350.00, 5, 13, 5),
(11, 'Calentador de agua', 3, 6, 180.00, 3, 14, 4),
(12, 'Ventilador de pie', 3, 8, 100.00, 2, 15, 2),
(13, 'Humidificador', 3, 7, 120.00, 1, 16, 3),
(14, 'Licuadora de cocina', 4, 7, 50.00, 1, 11, 1),
(15, 'Microondas', 4, 8, 80.00, 2, 12, 2),
(16, 'Procesador de alimentos', 4, 1, 150.00, 3, 13, 4),
(17, 'Batidora', 4, 2, 90.00, 2, 14, 3),
(18, 'Aspiradora', 5, 9, 120.00, 3, 15, 3),
(19, 'Detergente líquido', 5, 10, 10.00, 1, 16, 1),
(20, 'Mopa', 5, 9, 30.00, 2, 12, 2),
(21, 'Escoba eléctrica', 5, 10, 45.00, 3, 14, 3),
(22, 'Televisor 40 pulgadas', 6, 11, 400.00, 2, 15, 2),
(23, 'Equipo de sonido', 6, 12, 250.00, 3, 16, 3),
(24, 'Reproductor Blu-ray', 6, 11, 150.00, 2, 12, 1),
(25, 'Proyector', 6, 12, 300.00, 3, 13, 2),
(26, 'Maquinilla de afeitar eléctrica', 7, 13, 60.00, 4, 14, 1),
(27, 'Secadora de cabello', 7, 14, 40.00, 1, 15, 2),
(28, 'Cepillo de dientes eléctrico', 7, 13, 45.00, 2, 16, 3),
(29, 'Cortapelos', 7, 14, 70.00, 3, 11, 4),
(30, 'Filtro de agua', 8, 15, 25.00, 1, 12, 3),
(31, 'Repuesto para lavadora', 8, 16, 15.00, 2, 13, 1),
(32, 'Tapa para olla', 8, 15, 10.00, 3, 14, 2),
(33, 'Batería para control remoto', 8, 16, 5.00, 1, 15, 1),
(34, 'Estufa de gas', 1, 1, 150.00, 2, 11, 4),
(35, 'Horno eléctrico', 1, 2, 200.00, 3, 12, 5),
(36, 'Refrigerador', 1, 2, 400.00, 2, 13, 5),
(37, 'Cafetera', 1, 7, 80.00, 1, 14, 3),
(38, 'Tostadora', 1, 8, 60.00, 2, 15, 2),
(39, 'Lavadora automática', 2, 3, 500.00, 4, 16, 3),
(40, 'Secadora de ropa', 2, 4, 450.00, 2, 15, 2),
(41, 'Plancha de vapor', 2, 7, 70.00, 3, 12, 1),
(42, 'Secadora de manos', 2, 8, 90.00, 1, 11, 4),
(43, 'Aire acondicionado portátil', 3, 5, 350.00, 5, 13, 5),
(44, 'Calentador de agua', 3, 6, 180.00, 3, 14, 4),
(45, 'Ventilador de pie', 3, 8, 100.00, 2, 15, 2),
(46, 'Humidificador', 3, 7, 120.00, 1, 16, 3),
(47, 'Licuadora de cocina', 4, 7, 50.00, 1, 11, 1),
(48, 'Microondas', 4, 8, 80.00, 2, 12, 2),
(49, 'Procesador de alimentos', 4, 1, 150.00, 3, 13, 4),
(50, 'Batidora', 4, 2, 90.00, 2, 14, 3),
(51, 'Aspiradora', 5, 9, 120.00, 3, 15, 3),
(52, 'Detergente líquido', 5, 10, 10.00, 1, 16, 1),
(53, 'Mopa', 5, 9, 30.00, 2, 12, 2),
(54, 'Escoba eléctrica', 5, 10, 45.00, 3, 14, 3),
(55, 'Televisor 40 pulgadas', 6, 11, 400.00, 2, 15, 2),
(56, 'Equipo de sonido', 6, 12, 250.00, 3, 16, 3),
(57, 'Reproductor Blu-ray', 6, 11, 150.00, 2, 12, 1),
(58, 'Proyector', 6, 12, 300.00, 3, 13, 2),
(59, 'Maquinilla de afeitar eléctrica', 7, 13, 60.00, 4, 14, 1),
(60, 'Secadora de cabello', 7, 14, 40.00, 1, 15, 2),
(61, 'Cepillo de dientes eléctrico', 7, 13, 45.00, 2, 16, 3),
(62, 'Cortapelos', 7, 14, 70.00, 3, 11, 4),
(63, 'Filtro de agua', 8, 15, 25.00, 1, 12, 3),
(64, 'Repuesto para lavadora', 8, 16, 15.00, 2, 13, 1),
(65, 'Tapa para olla', 8, 15, 10.00, 3, 14, 2),
(66, 'Batería para control remoto', 8, 16, 5.00, 1, 15, 1),
(67, 'Estufa de gas', 1, 1, 150.00, 2, 11, 4),
(68, 'Horno eléctrico', 1, 2, 200.00, 3, 12, 5),
(69, 'Refrigerador', 1, 2, 400.00, 2, 13, 5),
(70, 'Cafetera', 1, 7, 80.00, 1, 14, 3),
(71, 'Tostadora', 1, 8, 60.00, 2, 15, 2),
(72, 'Lavadora automática', 2, 3, 500.00, 4, 16, 3),
(73, 'Secadora de ropa', 2, 4, 450.00, 2, 15, 2),
(74, 'Plancha de vapor', 2, 7, 70.00, 3, 12, 1),
(75, 'Secadora de manos', 2, 8, 90.00, 1, 11, 4),
(76, 'Aire acondicionado portátil', 3, 5, 350.00, 5, 13, 5),
(77, 'Calentador de agua', 3, 6, 180.00, 3, 14, 4),
(78, 'Ventilador de pie', 3, 8, 100.00, 2, 15, 2),
(79, 'Humidificador', 3, 7, 120.00, 1, 16, 3),
(80, 'Licuadora de cocina', 4, 7, 50.00, 1, 11, 1),
(81, 'Microondas', 4, 8, 80.00, 2, 12, 2),
(82, 'Procesador de alimentos', 4, 1, 150.00, 3, 13, 4),
(83, 'Batidora', 4, 2, 90.00, 2, 14, 3),
(84, 'Aspiradora', 5, 9, 120.00, 3, 15, 3),
(85, 'Detergente líquido', 5, 10, 10.00, 1, 16, 1),
(86, 'Mopa', 5, 9, 30.00, 2, 12, 2),
(87, 'Escoba eléctrica', 5, 10, 45.00, 3, 14, 3),
(88, 'Televisor 40 pulgadas', 6, 11, 400.00, 2, 15, 2),
(89, 'Equipo de sonido', 6, 12, 250.00, 3, 16, 3),
(90, 'Reproductor Blu-ray', 6, 11, 150.00, 2, 12, 1),
(91, 'Proyector', 6, 12, 300.00, 3, 13, 2),
(92, 'Maquinilla de afeitar eléctrica', 7, 13, 60.00, 4, 14, 1),
(93, 'Secadora de cabello', 7, 14, 40.00, 1, 15, 2),
(94, 'Cepillo de dientes eléctrico', 7, 13, 45.00, 2, 16, 3),
(95, 'Cortapelos', 7, 14, 70.00, 3, 11, 4),
(96, 'Filtro de agua', 8, 15, 25.00, 1, 12, 3),
(97, 'Repuesto para lavadora', 8, 16, 15.00, 2, 13, 1),
(98, 'Tapa para olla', 8, 15, 10.00, 3, 14, 2),
(99, 'Batería para control remoto', 8, 16, 5.00, 1, 15, 1),
(100, 'Cepillo de dientes manual', 7, 13, 10.00, 2, 16, 1);

--
-- Disparadores `producto`
--
DELIMITER $$
CREATE TRIGGER `after_insert_producto` AFTER INSERT ON `producto` FOR EACH ROW BEGIN
    INSERT INTO historicos_productos (
        id_producto, 
        accion, 
        fecha, 
        descripcion
    ) VALUES (
        NEW.id_producto, 
        'Insertar', 
        NOW(), 
        CONCAT('Se ha insertado el producto: ', NEW.nombre, ' con precio original: ', NEW.original_precio)
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_product_insert` AFTER INSERT ON `producto` FOR EACH ROW BEGIN
    INSERT INTO inventario (id_producto, id_categoria, cantidad_en_stock, stock_minimo, stock_maximo)
    VALUES (NEW.id_producto, NEW.id_categoria, 0, 0, 1000);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_update_producto` AFTER UPDATE ON `producto` FOR EACH ROW BEGIN
    INSERT INTO historicos_productos (
        id_producto, 
        accion, 
        fecha, 
        descripcion
    ) VALUES (
        NEW.id_producto, 
        'Actualizar', 
        NOW(), 
        CONCAT('Se ha actualizado el producto: ', NEW.nombre, ' de precio: ', OLD.original_precio, ' a: ', NEW.original_precio)
    );
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `before_delete_producto` BEFORE DELETE ON `producto` FOR EACH ROW BEGIN
    INSERT INTO historicos_productos (
        id_producto, 
        accion, 
        fecha, 
        descripcion
    ) VALUES (
        OLD.id_producto, 
        'Eliminar', 
        NOW(), 
        CONCAT('Se ha eliminado el producto: ', OLD.nombre, ' con precio: ', OLD.original_precio)
    );
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `promocion`
--

CREATE TABLE `promocion` (
  `id_promocion` int(100) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `valor` decimal(50,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `promocion`
--

INSERT INTO `promocion` (`id_promocion`, `nombre`, `valor`) VALUES
(11, 'Descuento de 5%', 0.05),
(12, 'Descuento de 10%', 0.10),
(13, 'Descuento de 15%', 0.15),
(14, 'Descuento de 20%', 0.20),
(15, 'Descuento de 25%', 0.25),
(16, 'Descuento de 30%', 0.30),
(17, 'Descuento de 40%', 0.40),
(18, 'Descuento de 50%', 0.50);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `Nombre_del_proveedor` varchar(50) NOT NULL,
  `Producto_Servicio` text NOT NULL,
  `Historial_de_desempeño` text NOT NULL,
  `nombre_compañia` varchar(20) NOT NULL,
  `Telefono` varchar(10) NOT NULL,
  `Ciudad` varchar(20) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `Documento` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `Nombre_del_proveedor`, `Producto_Servicio`, `Historial_de_desempeño`, `nombre_compañia`, `Telefono`, `Ciudad`, `tipo`, `Documento`) VALUES
(1, 'Luis Martínez', 'Estufas y hornos', 'Excelente', 'Cocina S.A.', '9876-1234', 'Tegucigalpa', 'RTN', '0801-2000-123'),
(2, 'María Rodríguez', 'Refrigeradores', 'Malo', 'Refrigeración Global', '2234-5678', 'San Pedro Sula', 'DNI', '1234567-A'),
(3, 'Carlos Gómez', 'Lavadoras', 'Bueno', 'Lavado y Secado Inc.', '3345-6789', 'La Ceiba', 'Pasaporte', 'HND1234567'),
(4, 'Ana Hernández', 'Secadoras', 'Muy bueno', 'Secado Total', '4456-7890', 'Comayagua', 'RTN', '1102-1999-654'),
(5, 'Pedro Fernández', 'Aires acondicionados', 'Excelente', 'Climatización Eficie', '5567-8901', 'Choluteca', 'DNI', '7654321-B'),
(6, 'Laura Morales', 'Calentadores', 'Bueno', 'Calor Confort', '6678-9012', 'Danlí', 'Pasaporte', 'HND7654321'),
(7, 'Jorge Pérez', 'Licuadoras', 'Muy bueno', 'Pequeños Electrodomé', '7789-0123', 'Santa Rosa de Copán', 'RTN', '1901-1988-123'),
(8, 'Sara Castillo', 'Microondas', 'Bueno', 'Cocina Fácil', '8890-1234', 'Puerto Cortés', 'DNI', '9876543-C'),
(9, 'Fernando Ruiz', 'Aspiradoras', 'Excelente', 'Limpieza Total', '9901-2345', 'Tela', 'RTN', '0203-2001-789'),
(10, 'Gloria Mejía', 'Detergentes', 'Muy bueno', 'Limpieza y Cía.', '1012-3456', 'El Progreso', 'Pasaporte', 'HND8765432'),
(11, 'Ricardo Díaz', 'Televisores', 'Excelente', 'Audio Video Express', '1123-4567', 'Juticalpa', 'RTN', '1401-2002-567'),
(12, 'Elena Solís', 'Equipos de sonido', 'Muy bueno', 'Sonido Perfecto', '2234-5678', 'Siguatepeque', 'DNI', '6543210-D'),
(13, 'Tomás García', 'Maquinillas de afeitar', 'Bueno', 'Cuidado Personal HN', '3345-6789', 'Santa Bárbara', 'Pasaporte', 'HND3456789'),
(14, 'Daniela Pérez', 'Secadoras de cabello', 'Muy bueno', 'Estilo Personal', '4456-7890', 'Ocotepeque', 'RTN', '1902-2003-098'),
(15, 'Adriana Reyes', 'Filtros de agua', 'Excelente', 'Accesorios Plus', '5567-8901', 'Gracias', 'RTN', '1002-2004-765'),
(16, 'Oscar Varela', 'Repuestos para lavadoras', 'Bueno', 'Repuestos Rápidos', '6678-9012', 'Nacaome', 'DNI', '3456789-E');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puesto_de_trabajo`
--

CREATE TABLE `puesto_de_trabajo` (
  `id_puesto` int(11) NOT NULL,
  `puesto_trabajo` varchar(50) DEFAULT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `salario` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `puesto_de_trabajo`
--

INSERT INTO `puesto_de_trabajo` (`id_puesto`, `puesto_trabajo`, `hora_inicio`, `hora_fin`, `salario`) VALUES
(3, 'Vendedor', '09:00:00', '17:00:00', 15000),
(4, 'Asesor de Ventas', '10:00:00', '18:00:00', 16000),
(5, 'Técnico de Reparaciones', '08:00:00', '16:00:00', 17000),
(6, 'Encargado de Inventario', '11:00:00', '19:00:00', 15500),
(7, 'Cajero', '12:00:00', '20:00:00', 14000),
(8, 'Asistente de Tienda', '09:00:00', '17:00:00', 14500),
(9, 'Gerente de Tienda', '08:00:00', '16:00:00', 20000),
(10, 'Auxiliar de Almacén', '10:00:00', '18:00:00', 13500),
(11, 'Atención al Cliente', '13:00:00', '21:00:00', 15000),
(12, 'Jefe de Ventas', '14:00:00', '22:00:00', 17500);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sar`
--

CREATE TABLE `sar` (
  `id_sar` int(11) NOT NULL,
  `rtn` varchar(16) NOT NULL,
  `cai` varchar(50) NOT NULL,
  `fecha_emision` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `rango_inicial` varchar(100) NOT NULL,
  `rango_final` varchar(100) NOT NULL,
  `id_sucursal` varchar(100) DEFAULT NULL,
  `secuencial` varchar(100) NOT NULL,
  `estado` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sar`
--

INSERT INTO `sar` (`id_sar`, `rtn`, `cai`, `fecha_emision`, `fecha_vencimiento`, `rango_inicial`, `rango_final`, `id_sucursal`, `secuencial`, `estado`) VALUES
(18, '0232-1616-266562', 'EN8ARA-CWID8D-K6L8F9-Y7NFKI-X2LAU9-N6', '2024-08-28', '2025-08-28', '00000150', '00000500', '1', '001', 'Activo'),
(19, '1984-6514-656266', 'G13X9Z-GQDGEQ-EBIQMM-JTE540-X489IN-91', '2024-08-28', '2025-08-28', '00000255', '00000400', '2', '002', 'Activo'),
(21, '1664-6865-646865', 'TAYT00-IFOYLZ-XV5Y0K-VBQYSQ-OEG6K2-07', '2024-08-28', '2025-08-28', '45134661', '99999999', '4', '004', 'Activo'),
(22, '0516-6549-466565', '5TJ8UM-92UTQR-CC9HUA-TKQVBN-7B1D15-DL', '2024-08-28', '2025-08-28', '00000000', '00000002', '3', '003', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguimiento_de_envio`
--

CREATE TABLE `seguimiento_de_envio` (
  `id_seguimiento` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL,
  `fecha_entrega_estimada` datetime DEFAULT NULL,
  `fecha_entrega_real` datetime DEFAULT NULL,
  `estado` varchar(100) NOT NULL,
  `id_transportista` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, 'Sucursal Central', '1689-4568'),
(2, 'Sucursal Norte', '2345-6789'),
(3, 'Sucursal Sur', '3456-7890'),
(4, 'Sucursal Este', '4567-8901'),
(5, 'Sucursal Oeste', '5678-9012'),
(6, 'Sucursal Aeropuerto', '0123-4567');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transportistas`
--

CREATE TABLE `transportistas` (
  `id_transportista` int(11) NOT NULL,
  `nombre_empresa` varchar(40) NOT NULL,
  `Telefono` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `transportistas`
--

INSERT INTO `transportistas` (`id_transportista`, `nombre_empresa`, `Telefono`) VALUES
(1, 'Transporte chipita', '9654-8969');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `primer_nombre` varchar(20) NOT NULL,
  `primer_apellido` varchar(20) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `usuario_activo` int(100) NOT NULL,
  `super_usuario` int(11) DEFAULT NULL,
  `id_sucursal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `primer_nombre`, `primer_apellido`, `correo`, `password`, `usuario_activo`, `super_usuario`, `id_sucursal`) VALUES
(18, 'ivan', 'joestar', 'ivans@gmail.com', '12345678', 1, 1, 2),
(20, 'Joshua', 'Martinez', 'joshua@gmail.com', 'joshua', 1, 0, 1),
(21, 'Dante', 'Valladares', 'dante@gmail.com', 'Dante123', 1, 0, 3),
(24, 'Renato', 'Lizardo', 'renato@gmail.com', 'Renato123', 1, 0, 4),
(26, 'Kevin', 'Zamora', 'kevin@gmail.com', '12345', 1, 0, 6),
(28, 'Luis', 'Melgar', 'luis@gmail.com', 'luis123', 1, 0, 5),
(29, 'melissa', 'oseguera', 'melissa@gmail.com', 'melissa123', 1, 0, 2);

--
-- Disparadores `usuarios`
--
DELIMITER $$
CREATE TRIGGER `update_empleado_after_usuario` AFTER UPDATE ON `usuarios` FOR EACH ROW BEGIN
    UPDATE empleados
    SET
        nombre = NEW.primer_nombre,
        apellido = NEW.primer_apellido,
        email = NEW.correo,
        password = NEW.password,
        id_sucursal = NEW.id_sucursal
    WHERE id_empleado = NEW.id_usuario;
END
$$
DELIMITER ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `almacenes`
--
ALTER TABLE `almacenes`
  ADD PRIMARY KEY (`id_almacenes`),
  ADD KEY `almacenes_FK` (`id_sucursal`);

--
-- Indices de la tabla `capacitacion`
--
ALTER TABLE `capacitacion`
  ADD PRIMARY KEY (`id_capacitacion`),
  ADD KEY `capacitacion_FK` (`id_empleado`);

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
-- Indices de la tabla `detalles_de_factura`
--
ALTER TABLE `detalles_de_factura`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `detalles_de_factura_FK` (`id_factura`),
  ADD KEY `detalles_de_factura_FK_1` (`id_producto`),
  ADD KEY `detalles_de_factura_FK_2` (`id_pedido`);

--
-- Indices de la tabla `detalle_de_compra_cliente`
--
ALTER TABLE `detalle_de_compra_cliente`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `detalle_de_compra_cliente_FK` (`id_pedido`);

--
-- Indices de la tabla `detalle_de_compra_proveedor`
--
ALTER TABLE `detalle_de_compra_proveedor`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `detalle_de_compra_proveedor_FK` (`id_pedido`),
  ADD KEY `detalle_de_compra_proveedor_FK_1` (`id_estado`),
  ADD KEY `detalle_de_compra_proveedor_FK_2` (`id_producto`),
  ADD KEY `detalle_de_compra_proveedor_FK_3` (`id_empleado`);

--
-- Indices de la tabla `devoluciones_compras`
--
ALTER TABLE `devoluciones_compras`
  ADD PRIMARY KEY (`id_devolucion`),
  ADD KEY `devoluciones_compra_FK` (`id_detalle`),
  ADD KEY `devoluciones_compra_FK_1` (`id_pedido`);

--
-- Indices de la tabla `devoluciones_ventas`
--
ALTER TABLE `devoluciones_ventas`
  ADD PRIMARY KEY (`id_devolucion`),
  ADD KEY `devoluciones_ventas_FK` (`id_detalle`),
  ADD KEY `devoluciones_ventas_FK_1` (`id_pedido`);

--
-- Indices de la tabla `distribucion_almacenes`
--
ALTER TABLE `distribucion_almacenes`
  ADD PRIMARY KEY (`id_distribucion`),
  ADD KEY `distribucion_almacenes_FK` (`id_producto`),
  ADD KEY `distribucion_almacenes_FK_1` (`id_almacenes_destino`),
  ADD KEY `distribucion_almacenes_FK_2` (`id_almacenes_origen`);

--
-- Indices de la tabla `documentacion_clientes`
--
ALTER TABLE `documentacion_clientes`
  ADD PRIMARY KEY (`id_documentoc`);

--
-- Indices de la tabla `documento_empleado`
--
ALTER TABLE `documento_empleado`
  ADD PRIMARY KEY (`id_documento`),
  ADD UNIQUE KEY `documento` (`documento`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`),
  ADD KEY `empleados_FK` (`id_sucursal`);

--
-- Indices de la tabla `equipo`
--
ALTER TABLE `equipo`
  ADD PRIMARY KEY (`id_equipo`);

--
-- Indices de la tabla `estado`
--
ALTER TABLE `estado`
  ADD PRIMARY KEY (`id_estado`);

--
-- Indices de la tabla `factu`
--
ALTER TABLE `factu`
  ADD PRIMARY KEY (`id_factura`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`id_factura`),
  ADD KEY `factura_FK_1` (`id_sar`),
  ADD KEY `factura_FK` (`id_impuesto`),
  ADD KEY `factura_FK_2` (`id_pedido`),
  ADD KEY `factura_FK_3` (`id_producto`);

--
-- Indices de la tabla `garantia`
--
ALTER TABLE `garantia`
  ADD PRIMARY KEY (`id_garantia`);

--
-- Indices de la tabla `historial_de_pagos`
--
ALTER TABLE `historial_de_pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `historial_de_pagos_FK` (`id_cliente`),
  ADD KEY `historial_de_pagos_FK_1` (`id_factura`),
  ADD KEY `historial_de_pagos_FK_2` (`id_metodo`);

--
-- Indices de la tabla `historicos_almacenes`
--
ALTER TABLE `historicos_almacenes`
  ADD PRIMARY KEY (`id_historicos`),
  ADD KEY `historicos_almacenes_FK` (`id_almacenes`);

--
-- Indices de la tabla `historicos_clientes`
--
ALTER TABLE `historicos_clientes`
  ADD PRIMARY KEY (`id_historico`),
  ADD KEY `historicos_clientes_FK` (`id_cliente`);

--
-- Indices de la tabla `historicos_devolucion`
--
ALTER TABLE `historicos_devolucion`
  ADD PRIMARY KEY (`id_historico`),
  ADD KEY `historicos_devolucion_FK` (`id_devolucion`);

--
-- Indices de la tabla `historicos_empleados`
--
ALTER TABLE `historicos_empleados`
  ADD PRIMARY KEY (`id_historico`),
  ADD KEY `historicos_empleados_FK` (`id_empleado`);

--
-- Indices de la tabla `historicos_impuestos`
--
ALTER TABLE `historicos_impuestos`
  ADD PRIMARY KEY (`id_historico`),
  ADD KEY `historicos_impuestos_FK` (`id_impuesto`);

--
-- Indices de la tabla `historicos_productos`
--
ALTER TABLE `historicos_productos`
  ADD PRIMARY KEY (`id_historico`),
  ADD KEY `historicos_productos_FK` (`id_producto`);

--
-- Indices de la tabla `ideas_mejora`
--
ALTER TABLE `ideas_mejora`
  ADD PRIMARY KEY (`id_mejora`);

--
-- Indices de la tabla `impuesto`
--
ALTER TABLE `impuesto`
  ADD PRIMARY KEY (`id_impuesto`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_inventario`),
  ADD KEY `inventario_FK` (`id_producto`),
  ADD KEY `inventario_FK_1` (`id_categoria`);

--
-- Indices de la tabla `inventario_almacenes`
--
ALTER TABLE `inventario_almacenes`
  ADD PRIMARY KEY (`id_inventario_almacenes`),
  ADD KEY `inventario_almacenes_FK` (`id_almacenes`),
  ADD KEY `inventario_almacenes_FK_1` (`id_producto`);

--
-- Indices de la tabla `mantenimiento_equipo`
--
ALTER TABLE `mantenimiento_equipo`
  ADD PRIMARY KEY (`id_mantenimiento`),
  ADD KEY `mantenimiento_equipo_FK` (`id_equipo`);

--
-- Indices de la tabla `metodo_de_pago`
--
ALTER TABLE `metodo_de_pago`
  ADD PRIMARY KEY (`id_metodo`);

--
-- Indices de la tabla `pedido_de_compra_cliente`
--
ALTER TABLE `pedido_de_compra_cliente`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `pedido_de_compra_cliente__FK` (`id_cliente`),
  ADD KEY `pedido_de_compra_cliente__FK_2` (`id_metodo`),
  ADD KEY `pedido_de_compra_cliente__FK_1` (`id_estado`),
  ADD KEY `pedido_de_compra_cliente_FK` (`id_sucursal`),
  ADD KEY `pedido_de_compra_cliente_FK_1` (`id_empleado`);

--
-- Indices de la tabla `pedido_de_compra_proveedor`
--
ALTER TABLE `pedido_de_compra_proveedor`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `pedido_de_compra_proveedor__FK_1` (`id_proveedor`),
  ADD KEY `pedido_de_compra_proveedor__FK_2` (`id_metodo`),
  ADD KEY `pedido_de_compra_proveedor__FK` (`id_estado`),
  ADD KEY `pedido_de_compra_proveedor_FK` (`id_empleado`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `producto_FK` (`id_categoria`),
  ADD KEY `producto_FK_1` (`id_proveedor`),
  ADD KEY `producto_FK_2` (`id_impuesto`),
  ADD KEY `producto_FK_3` (`id_promocion`),
  ADD KEY `producto_FK_4` (`id_garantia`);

--
-- Indices de la tabla `promocion`
--
ALTER TABLE `promocion`
  ADD PRIMARY KEY (`id_promocion`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `puesto_de_trabajo`
--
ALTER TABLE `puesto_de_trabajo`
  ADD PRIMARY KEY (`id_puesto`);

--
-- Indices de la tabla `sar`
--
ALTER TABLE `sar`
  ADD PRIMARY KEY (`id_sar`),
  ADD KEY `sar_FK` (`id_sucursal`);

--
-- Indices de la tabla `seguimiento_de_envio`
--
ALTER TABLE `seguimiento_de_envio`
  ADD PRIMARY KEY (`id_seguimiento`),
  ADD KEY `seguimiento_de_envio_FK` (`id_pedido`),
  ADD KEY `seguimiento_de_envio_FK_1` (`id_transportista`);

--
-- Indices de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  ADD PRIMARY KEY (`id_sucursal`);

--
-- Indices de la tabla `transportistas`
--
ALTER TABLE `transportistas`
  ADD PRIMARY KEY (`id_transportista`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `usuarios_FK` (`id_sucursal`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `almacenes`
--
ALTER TABLE `almacenes`
  MODIFY `id_almacenes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `capacitacion`
--
ALTER TABLE `capacitacion`
  MODIFY `id_capacitacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `detalles_de_factura`
--
ALTER TABLE `detalles_de_factura`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_de_compra_cliente`
--
ALTER TABLE `detalle_de_compra_cliente`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `detalle_de_compra_proveedor`
--
ALTER TABLE `detalle_de_compra_proveedor`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `devoluciones_compras`
--
ALTER TABLE `devoluciones_compras`
  MODIFY `id_devolucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `devoluciones_ventas`
--
ALTER TABLE `devoluciones_ventas`
  MODIFY `id_devolucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `distribucion_almacenes`
--
ALTER TABLE `distribucion_almacenes`
  MODIFY `id_distribucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `documentacion_clientes`
--
ALTER TABLE `documentacion_clientes`
  MODIFY `id_documentoc` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `documento_empleado`
--
ALTER TABLE `documento_empleado`
  MODIFY `id_documento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `equipo`
--
ALTER TABLE `equipo`
  MODIFY `id_equipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3031;

--
-- AUTO_INCREMENT de la tabla `estado`
--
ALTER TABLE `estado`
  MODIFY `id_estado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `factu`
--
ALTER TABLE `factu`
  MODIFY `id_factura` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
  MODIFY `id_factura` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `garantia`
--
ALTER TABLE `garantia`
  MODIFY `id_garantia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `historial_de_pagos`
--
ALTER TABLE `historial_de_pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `historicos_almacenes`
--
ALTER TABLE `historicos_almacenes`
  MODIFY `id_historicos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `historicos_clientes`
--
ALTER TABLE `historicos_clientes`
  MODIFY `id_historico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `historicos_devolucion`
--
ALTER TABLE `historicos_devolucion`
  MODIFY `id_historico` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `historicos_empleados`
--
ALTER TABLE `historicos_empleados`
  MODIFY `id_historico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT de la tabla `historicos_impuestos`
--
ALTER TABLE `historicos_impuestos`
  MODIFY `id_historico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `historicos_productos`
--
ALTER TABLE `historicos_productos`
  MODIFY `id_historico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=355;

--
-- AUTO_INCREMENT de la tabla `ideas_mejora`
--
ALTER TABLE `ideas_mejora`
  MODIFY `id_mejora` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `impuesto`
--
ALTER TABLE `impuesto`
  MODIFY `id_impuesto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_inventario` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=208;

--
-- AUTO_INCREMENT de la tabla `inventario_almacenes`
--
ALTER TABLE `inventario_almacenes`
  MODIFY `id_inventario_almacenes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `mantenimiento_equipo`
--
ALTER TABLE `mantenimiento_equipo`
  MODIFY `id_mantenimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `metodo_de_pago`
--
ALTER TABLE `metodo_de_pago`
  MODIFY `id_metodo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `pedido_de_compra_cliente`
--
ALTER TABLE `pedido_de_compra_cliente`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT de la tabla `pedido_de_compra_proveedor`
--
ALTER TABLE `pedido_de_compra_proveedor`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT de la tabla `promocion`
--
ALTER TABLE `promocion`
  MODIFY `id_promocion` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `puesto_de_trabajo`
--
ALTER TABLE `puesto_de_trabajo`
  MODIFY `id_puesto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `sar`
--
ALTER TABLE `sar`
  MODIFY `id_sar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  MODIFY `id_sucursal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `transportistas`
--
ALTER TABLE `transportistas`
  MODIFY `id_transportista` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `almacenes`
--
ALTER TABLE `almacenes`
  ADD CONSTRAINT `almacenes_FK` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursales` (`id_sucursal`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `capacitacion`
--
ALTER TABLE `capacitacion`
  ADD CONSTRAINT `capacitacion_FK` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalles_de_factura`
--
ALTER TABLE `detalles_de_factura`
  ADD CONSTRAINT `detalles_de_factura_FK` FOREIGN KEY (`id_factura`) REFERENCES `factura` (`id_factura`) ON UPDATE CASCADE,
  ADD CONSTRAINT `detalles_de_factura_FK_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON UPDATE CASCADE,
  ADD CONSTRAINT `detalles_de_factura_FK_2` FOREIGN KEY (`id_pedido`) REFERENCES `pedido_de_compra_cliente` (`id_pedido`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalle_de_compra_cliente`
--
ALTER TABLE `detalle_de_compra_cliente`
  ADD CONSTRAINT `detalle_de_compra_cliente_FK` FOREIGN KEY (`id_pedido`) REFERENCES `pedido_de_compra_cliente` (`id_pedido`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalle_de_compra_proveedor`
--
ALTER TABLE `detalle_de_compra_proveedor`
  ADD CONSTRAINT `detalle_de_compra_proveedor_FK` FOREIGN KEY (`id_pedido`) REFERENCES `pedido_de_compra_proveedor` (`id_pedido`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `detalle_de_compra_proveedor_FK_1` FOREIGN KEY (`id_estado`) REFERENCES `estado` (`id_estado`) ON UPDATE CASCADE,
  ADD CONSTRAINT `detalle_de_compra_proveedor_FK_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `detalle_de_compra_proveedor_FK_3` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `devoluciones_compras`
--
ALTER TABLE `devoluciones_compras`
  ADD CONSTRAINT `devoluciones_compra_FK` FOREIGN KEY (`id_detalle`) REFERENCES `detalle_de_compra_proveedor` (`id_detalle`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `devoluciones_compra_FK_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido_de_compra_proveedor` (`id_pedido`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `empleados_FK` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursales` (`id_sucursal`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `factura_FK` FOREIGN KEY (`id_impuesto`) REFERENCES `impuesto` (`id_impuesto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `factura_FK_1` FOREIGN KEY (`id_sar`) REFERENCES `sar` (`id_sar`) ON UPDATE CASCADE,
  ADD CONSTRAINT `factura_FK_2` FOREIGN KEY (`id_pedido`) REFERENCES `pedido_de_compra_cliente` (`id_pedido`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `factura_FK_3` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `pedido_de_compra_cliente`
--
ALTER TABLE `pedido_de_compra_cliente`
  ADD CONSTRAINT `pedido_de_compra_cliente_FK` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursales` (`id_sucursal`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `pedido_de_compra_cliente_FK_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `pedido_de_compra_proveedor`
--
ALTER TABLE `pedido_de_compra_proveedor`
  ADD CONSTRAINT `pedido_de_compra_proveedor_FK` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
