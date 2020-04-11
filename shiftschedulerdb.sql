--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

-- Started on 2020-04-04 21:26:18

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 16725)
-- Name: coordinators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.coordinators (
    netid text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL
);


ALTER TABLE public.coordinators OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16733)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    netid text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    hours double precision,
    total_hours double precision,
    manager boolean
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16808)
-- Name: shift_assign; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shift_assign (
    netid text NOT NULL,
    shift_id integer NOT NULL
);


ALTER TABLE public.shift_assign OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16814)
-- Name: shift_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shift_info (
    shift_id bigint,
    date date,
    task_id integer,
    cur_people integer
);


ALTER TABLE public.shift_info OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16820)
-- Name: task_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_info (
    task_id integer NOT NULL,
    meal text NOT NULL,
    task text NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    min_people integer NOT NULL,
    max_people integer NOT NULL,
    pay_level character(1) NOT NULL
);


ALTER TABLE public.task_info OWNER TO postgres;

--
-- TOC entry 2838 (class 0 OID 16725)
-- Dependencies: 202
-- Data for Name: coordinators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.coordinators (netid, first_name, last_name) FROM stdin;
agurgen	Ali Ekin	Gurgen
mnagdee	Masi	Nagdee
\.


--
-- TOC entry 2839 (class 0 OID 16733)
-- Dependencies: 203
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (netid, first_name, last_name, hours, total_hours, manager) FROM stdin;
mnagdee	Masi	Nagdee	0	0	\N
ortaoglu	Begum	Ortaoglu	0	0	\N
cz10	Cheyenne	Zhang	0	0	\N
trt2	Theo	Trevisan	0	0	\N
tguy	test	guy	1	1	\N
\.


--
-- TOC entry 2840 (class 0 OID 16808)
-- Dependencies: 204
-- Data for Name: shift_assign; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shift_assign (netid, shift_id) FROM stdin;
ortaoglu	123
ortaoglu	234
trt2	234
\.


--
-- TOC entry 2841 (class 0 OID 16814)
-- Dependencies: 205
-- Data for Name: shift_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shift_info (shift_id, date, task_id, cur_people) FROM stdin;
123	2020-03-23	1	2
124	2020-03-23	2	1
125	2020-03-23	3	5
126	2020-03-23	4	1
127	2020-03-23	5	2
128	2020-03-23	6	4
129	2020-03-24	1	1
130	2020-03-28	7	1
131	2020-03-28	8	2
132	2020-03-28	9	6
133	2020-03-28	10	2
134	2020-03-28	11	3
135	2020-03-28	12	3
\.


--
-- TOC entry 2842 (class 0 OID 16820)
-- Dependencies: 206
-- Data for Name: task_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_info (task_id, meal, task, start_time, end_time, min_people, max_people, pay_level) FROM stdin;
2	Dinner	First Shift	04:45:00	07:30:00	2	2	B
3	Dinner	Second Shift	19:15:00	21:00:00	4	6	B
4	Dinner	Dish Manager	17:00:00	21:00:00	2	2	A
5	Dinner	First Dish	17:15:00	19:15:00	2	4	B
6	Dinner	Second Dish	19:00:00	21:00:00	2	4	B
7	Brunch	Manager	09:45:00	15:00:00	0	2	A
8	Brunch	First Shift	10:45:00	13:30:00	1	2	B
9	Brunch	Second Shift	13:15:00	15:00:00	5	6	B
10	Brunch	Dish Manager	10:30:00	15:00:00	0	2	A
11	Brunch	First Dish	11:15:00	13:15:00	3	4	B
12	Brunch	Second Dish	13:00:00	15:00:00	3	4	B
13	CJL	CJL Swipe	17:00:00	21:00:00	1	1	B
1	Dinner	Manager	04:30:00	09:00:00	2	2	A
\.


--
-- TOC entry 2709 (class 2606 OID 16740)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (netid);


--
-- TOC entry 2707 (class 2606 OID 16732)
-- Name: coordinators employers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coordinators
    ADD CONSTRAINT employers_pkey PRIMARY KEY (netid);


--
-- TOC entry 2711 (class 2606 OID 16827)
-- Name: task_info task_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_info
    ADD CONSTRAINT task_info_pkey PRIMARY KEY (task_id);


-- Completed on 2020-04-04 21:26:18

--
-- PostgreSQL database dump complete
--

