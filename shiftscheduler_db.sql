PGDMP                         x            shiftscheduler    12.2    12.2                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16724    shiftscheduler    DATABASE     �   CREATE DATABASE shiftscheduler WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE shiftscheduler;
                postgres    false            �            1259    16733 	   employees    TABLE     �   CREATE TABLE public.employees (
    netid text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    hours double precision,
    total_hours double precision
);
    DROP TABLE public.employees;
       public         heap    postgres    false            �            1259    16725 	   employers    TABLE     v   CREATE TABLE public.employers (
    netid text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL
);
    DROP TABLE public.employers;
       public         heap    postgres    false            �            1259    16779    shift_assignments    TABLE     Z   CREATE TABLE public.shift_assignments (
    shift_id bigint NOT NULL,
    netid text[]
);
 %   DROP TABLE public.shift_assignments;
       public         heap    postgres    false            �            1259    16749    shifts    TABLE     �   CREATE TABLE public.shifts (
    shift_id bigint NOT NULL,
    date date NOT NULL,
    meal text NOT NULL,
    "position" text NOT NULL,
    min_people smallint NOT NULL,
    max_people smallint NOT NULL,
    cur_people smallint NOT NULL
);
    DROP TABLE public.shifts;
       public         heap    postgres    false                      0    16733 	   employees 
   TABLE DATA           U   COPY public.employees (netid, first_name, last_name, hours, total_hours) FROM stdin;
    public          postgres    false    203                     0    16725 	   employers 
   TABLE DATA           A   COPY public.employers (netid, first_name, last_name) FROM stdin;
    public          postgres    false    202   k                 0    16779    shift_assignments 
   TABLE DATA           <   COPY public.shift_assignments (shift_id, netid) FROM stdin;
    public          postgres    false    205   �                 0    16749    shifts 
   TABLE DATA           f   COPY public.shifts (shift_id, date, meal, "position", min_people, max_people, cur_people) FROM stdin;
    public          postgres    false    204   �       �
           2606    16740    employees employees_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (netid);
 B   ALTER TABLE ONLY public.employees DROP CONSTRAINT employees_pkey;
       public            postgres    false    203            �
           2606    16732    employers employers_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.employers
    ADD CONSTRAINT employers_pkey PRIMARY KEY (netid);
 B   ALTER TABLE ONLY public.employers DROP CONSTRAINT employers_pkey;
       public            postgres    false    202            �
           2606    16786 (   shift_assignments shift_assignments_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.shift_assignments
    ADD CONSTRAINT shift_assignments_pkey PRIMARY KEY (shift_id);
 R   ALTER TABLE ONLY public.shift_assignments DROP CONSTRAINT shift_assignments_pkey;
       public            postgres    false    205            �
           2606    16756    shifts shifts_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shifts_pkey PRIMARY KEY (shift_id);
 <   ALTER TABLE ONLY public.shifts DROP CONSTRAINT shifts_pkey;
       public            postgres    false    204               [   x�5�M@0F�_#�����	�i�&UN/���	J�0��ͣ���2EYw�,{@���櫴h�����=�\ap1$>�F��0�ܿ��         2   x�KL/-JO��t��Tp����t�r��SRS9}�39��l�=... ���         $   x�3��/*I�O�)�))*1��2B��r��qqq �M�         =   x�3�4202�50�52�L*JM�NK,.���/�M��4�4�4�2BV�S����,o����� ��f     