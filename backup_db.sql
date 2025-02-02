PGDMP      &                |         
   coursework    16.3    16.3 c               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    26337 
   coursework    DATABASE     ~   CREATE DATABASE coursework WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE coursework;
                postgres    false            �            1255    26518 [   add_participant(character varying, character varying, character varying, character varying)    FUNCTION     @  CREATE FUNCTION public.add_participant(surname character varying, first_name character varying, role character varying, contact character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO participants (surname, name, role, contact_info)
    VALUES (surname, first_name, role, contact);
END;
$$;
 �   DROP FUNCTION public.add_participant(surname character varying, first_name character varying, role character varying, contact character varying);
       public          postgres    false            �            1255    26515 J   add_publication(integer, character varying, character varying, text, date)    FUNCTION     9  CREATE FUNCTION public.add_publication(smi_id integer, cat character varying, tit character varying, sum text, pub_date date) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO publications (id_smi, category, title, summary, publication_date)
    VALUES (smi_id, cat, tit, sum, pub_date);
END;
$$;
 }   DROP FUNCTION public.add_publication(smi_id integer, cat character varying, tit character varying, sum text, pub_date date);
       public          postgres    false            �            1255    26521 4   add_relationship(integer, integer, double precision)    FUNCTION       CREATE FUNCTION public.add_relationship(pub_id integer, part_id integer, price double precision) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO participantAndPublicatonsRelationship (id_publication, id_participant, price)
    VALUES (pub_id, part_id, price);
END;
$$;
 `   DROP FUNCTION public.add_relationship(pub_id integer, part_id integer, price double precision);
       public          postgres    false            �            1255    26512 @   add_smi(character varying, character varying, character varying)    FUNCTION     
  CREATE FUNCTION public.add_smi(smi_name character varying, smi_type character varying, smi_contact character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO smi (name, type, contact_info) VALUES (smi_name, smi_type, smi_contact);
END;
$$;
 u   DROP FUNCTION public.add_smi(smi_name character varying, smi_type character varying, smi_contact character varying);
       public          postgres    false                       1255    26526    avg_participation_price()    FUNCTION       CREATE FUNCTION public.avg_participation_price() RETURNS double precision
    LANGUAGE plpgsql
    AS $$
DECLARE
    avg_price DOUBLE PRECISION;
BEGIN
    SELECT AVG(price) INTO avg_price FROM participantAndPublicatonsRelationship;
    RETURN avg_price;
END;
$$;
 0   DROP FUNCTION public.avg_participation_price();
       public          postgres    false            �            1255    26520    delete_participant(integer)    FUNCTION     �   CREATE FUNCTION public.delete_participant(part_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM participants WHERE id_participant = part_id;
END;
$$;
 :   DROP FUNCTION public.delete_participant(part_id integer);
       public          postgres    false            �            1255    26517    delete_publication(integer)    FUNCTION     �   CREATE FUNCTION public.delete_publication(pub_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM publications WHERE id_publication = pub_id;
END;
$$;
 9   DROP FUNCTION public.delete_publication(pub_id integer);
       public          postgres    false                       1255    26546    delete_publication_details()    FUNCTION     �  CREATE FUNCTION public.delete_publication_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM participantAndPublicatonsRelationship
    WHERE id_publication = OLD.id_publication AND id_participant = (SELECT id_participant FROM participants WHERE name = OLD.participant_name LIMIT 1);

    DELETE FROM publications WHERE id_publication = OLD.id_publication;

    RETURN OLD;
END;
$$;
 3   DROP FUNCTION public.delete_publication_details();
       public          postgres    false                       1255    26542    delete_publication_history()    FUNCTION     v  CREATE FUNCTION public.delete_publication_history() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO publications_history (id_publication, category, title, summary, publication_date, last_edited, change_type)
    VALUES (OLD.id_publication, OLD.category, OLD.title, OLD.summary, OLD.publication_date, OLD.last_edited, 'DELETE');
    RETURN OLD;
END;
$$;
 3   DROP FUNCTION public.delete_publication_history();
       public          postgres    false            �            1255    26523    delete_relationship(integer)    FUNCTION     �   CREATE FUNCTION public.delete_relationship(rel_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM participantAndPublicatonsRelationship WHERE id_relationship = rel_id;
END;
$$;
 :   DROP FUNCTION public.delete_relationship(rel_id integer);
       public          postgres    false            �            1255    26514    delete_smi(integer)    FUNCTION     �   CREATE FUNCTION public.delete_smi(smi_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM smi WHERE id_smi = smi_id;
END;
$$;
 1   DROP FUNCTION public.delete_smi(smi_id integer);
       public          postgres    false                       1255    26544    insert_publication_details()    FUNCTION     1  CREATE FUNCTION public.insert_publication_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    smi_id INT;
    participant_id INT;
BEGIN
    SELECT id_smi INTO smi_id FROM smi WHERE name = NEW.media_name LIMIT 1;
    IF NOT FOUND THEN
        INSERT INTO smi (name, type, contact_info) VALUES (NEW.media_name, '', '') RETURNING id_smi INTO smi_id;
    END IF;

    SELECT id_participant INTO participant_id FROM participants WHERE name = NEW.participant_name LIMIT 1;
    IF NOT FOUND THEN
        INSERT INTO participants (name, surname, role, contact_info) VALUES (NEW.participant_name, '', '', '') RETURNING id_participant INTO participant_id;
    END IF;

	INSERT INTO publications (id_smi, category, title, summary, publication_date, last_edited) 
    VALUES (smi_id, '', NEW.title, '', CURRENT_DATE, CURRENT_TIMESTAMP) RETURNING id_publication INTO NEW.id_publication;

    INSERT INTO participantAndPublicatonsRelationship (id_publication, id_participant, price) 
    VALUES (NEW.id_publication, participant_id, NEW.price);

    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.insert_publication_details();
       public          postgres    false                       1255    26538    insert_publication_history()    FUNCTION     v  CREATE FUNCTION public.insert_publication_history() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO publications_history (id_publication, category, title, summary, publication_date, last_edited, change_type)
    VALUES (NEW.id_publication, NEW.category, NEW.title, NEW.summary, NEW.publication_date, NEW.last_edited, 'INSERT');
    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.insert_publication_history();
       public          postgres    false            �            1255    26508    participant_delete_log()    FUNCTION       CREATE FUNCTION public.participant_delete_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO logs (log_level, message) 
    VALUES ('INFO', 'Участник удален: ' || OLD.name || ' ' || OLD.surname);
    RETURN OLD;
END;
$$;
 /   DROP FUNCTION public.participant_delete_log();
       public          postgres    false                       1255    26551 5   price_avg_accum(double precision[], double precision)    FUNCTION     A  CREATE FUNCTION public.price_avg_accum(state double precision[], price double precision) RETURNS double precision[]
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF state IS NULL THEN
        state := ARRAY[0.0, 0]; 
    END IF;
    state[1] := state[1] + price; 
    state[2] := state[2] + 1;     
    RETURN state;
END;
$$;
 X   DROP FUNCTION public.price_avg_accum(state double precision[], price double precision);
       public          postgres    false            	           1255    26552 #   price_avg_final(double precision[])    FUNCTION       CREATE FUNCTION public.price_avg_final(state double precision[]) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF state IS NULL OR state[2] = 0 THEN
        RETURN NULL; 
    ELSE
        RETURN state[1] / state[2]; 
    END IF;
END;
$$;
 @   DROP FUNCTION public.price_avg_final(state double precision[]);
       public          postgres    false                       1255    26525 �   process_publication_update(integer, character varying, text, date, integer, character varying, character varying, double precision) 	   PROCEDURE     �  CREATE PROCEDURE public.process_publication_update(IN pub_id integer, IN new_title character varying, IN new_summary text, IN new_publication_date date, IN part_id integer, IN new_surname character varying, IN new_contact_info character varying, IN new_price double precision)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Открытие транзакции (неявное для процедур PL/pgSQL)
    -- Обновление данных публикации
    UPDATE publications SET
        title = new_title,
        summary = new_summary,
        publication_date = new_publication_date
    WHERE id_publication = pub_id;

    -- Обновление данных участника
    UPDATE participants SET
        surname = new_surname,
        contact_info = new_contact_info
    WHERE id_participant = part_id;

    -- Добавление новой связи между публикацией и участником
    INSERT INTO participantAndPublicatonsRelationship (id_publication, id_participant, price)
    VALUES (pub_id, part_id, new_price);

    -- Транзакция будет автоматически подтверждена после успешного завершения процедуры
EXCEPTION
    WHEN OTHERS THEN
        -- Откат изменений, если произошла ошибка
        ROLLBACK;
        -- Логирование ошибки или уведомление
        RAISE NOTICE 'Transaction failed: %', SQLERRM;
END;
$$;
   DROP PROCEDURE public.process_publication_update(IN pub_id integer, IN new_title character varying, IN new_summary text, IN new_publication_date date, IN part_id integer, IN new_surname character varying, IN new_contact_info character varying, IN new_price double precision);
       public          postgres    false            �            1255    26510    relationship_insert_log()    FUNCTION     <  CREATE FUNCTION public.relationship_insert_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO logs (log_level, message) 
    VALUES ('INFO', 'Новая связь создана: Publication ID ' || NEW.id_publication || ' - Participant ID ' || NEW.id_participant);
    RETURN NEW;
END;
$$;
 0   DROP FUNCTION public.relationship_insert_log();
       public          postgres    false            �            1255    26504    smi_insert_log()    FUNCTION     �   CREATE FUNCTION public.smi_insert_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO logs (log_level, message) 
    VALUES ('INFO', 'Новое СМИ добавлено: ' || NEW.name);
    RETURN NEW;
END;
$$;
 '   DROP FUNCTION public.smi_insert_log();
       public          postgres    false            �            1255    26506    update_last_edited()    FUNCTION     x  CREATE FUNCTION public.update_last_edited() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF (OLD.title <> NEW.title OR OLD.summary <> NEW.summary) THEN
        NEW.last_edited = CURRENT_TIMESTAMP;
        INSERT INTO logs (log_level, message) 
        VALUES ('INFO', 'Публикация обновлена: ' || NEW.title);
    END IF;
    RETURN NEW;
END;
$$;
 +   DROP FUNCTION public.update_last_edited();
       public          postgres    false            �            1255    26519 g   update_participant(integer, character varying, character varying, character varying, character varying)    FUNCTION     �  CREATE FUNCTION public.update_participant(part_id integer, new_surname character varying, new_first_name character varying, new_role character varying, new_contact character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE participants 
    SET 
        surname = new_surname, 
        name = new_first_name, 
        role = new_role, 
        contact_info = new_contact
    WHERE id_participant = part_id;
END;
$$;
 �   DROP FUNCTION public.update_participant(part_id integer, new_surname character varying, new_first_name character varying, new_role character varying, new_contact character varying);
       public          postgres    false            �            1255    26516 V   update_publication(integer, integer, character varying, character varying, text, date)    FUNCTION     d  CREATE FUNCTION public.update_publication(pub_id integer, smi_id integer, cat character varying, tit character varying, sum text, pub_date date) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE publications SET id_smi = smi_id, category = cat, title = tit, summary = sum, publication_date = pub_date
    WHERE id_publication = pub_id;
END;
$$;
 �   DROP FUNCTION public.update_publication(pub_id integer, smi_id integer, cat character varying, tit character varying, sum text, pub_date date);
       public          postgres    false            �            1255    26498    update_publication_details()    FUNCTION     �  CREATE FUNCTION public.update_publication_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Обновление заголовка публикации, если изменился
    IF OLD.title <> NEW.title THEN
        UPDATE publications
        SET title = NEW.title
        WHERE id_publication = NEW.id_publication;
    END IF;

    -- Обновление имени СМИ, если изменилось
    IF OLD.media_name <> NEW.media_name THEN
        UPDATE smi
        SET name = NEW.media_name
        WHERE id_smi = (SELECT id_smi 
                        FROM publications 
                        WHERE id_publication = NEW.id_publication);
    END IF;

    -- Обновление имени участника, если изменилось
    IF OLD.participant_name <> NEW.participant_name THEN
        UPDATE participants
        SET name = NEW.participant_name
        WHERE id_participant = (SELECT id_participant
                                FROM participantAndPublicatonsRelationship
                                WHERE id_publication = NEW.id_publication);
    END IF;

    -- Обновление цены участия, если изменилась
    IF OLD.price <> NEW.price THEN
        UPDATE participantAndPublicatonsRelationship
        SET price = NEW.price
        WHERE id_publication = NEW.id_publication AND id_participant = (SELECT id_participant 
                                                                       FROM participants 
                                                                       WHERE name = OLD.participant_name LIMIT 1);
    END IF;

    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.update_publication_details();
       public          postgres    false                       1255    26540    update_publication_history()    FUNCTION     v  CREATE FUNCTION public.update_publication_history() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO publications_history (id_publication, category, title, summary, publication_date, last_edited, change_type)
    VALUES (OLD.id_publication, OLD.category, OLD.title, OLD.summary, OLD.publication_date, OLD.last_edited, 'UPDATE');
    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.update_publication_history();
       public          postgres    false                        1255    26524    update_publication_prices()    FUNCTION     �  CREATE FUNCTION public.update_publication_prices() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    -- Объявление переменных для хранения данных каждой строки
    rel_record participantAndPublicatonsRelationship%ROWTYPE;
    new_price DOUBLE PRECISION;
    cur CURSOR FOR SELECT * FROM participantAndPublicatonsRelationship; -- Курсор для всех записей
BEGIN
    -- Открытие курсора
    OPEN cur;
    
    -- Цикл по всем записям в курсоре
    LOOP
        FETCH cur INTO rel_record; -- Извлечение следующей записи
        EXIT WHEN NOT FOUND; -- Выход из цикла, если записи закончились

        -- Вычисление новой цены
        new_price := (rel_record.price * 1.10)text; -- Увеличение цены на 10%

        -- Обновление цены в таблице
        UPDATE participantAndPublicatonsRelationship
        SET price = new_price
        WHERE id_relationship = rel_record.id_relationship;
    END LOOP;
    
    -- Закрытие курсора
    CLOSE cur;
END;
$$;
 2   DROP FUNCTION public.update_publication_prices();
       public          postgres    false            �            1255    26522 @   update_relationship(integer, integer, integer, double precision)    FUNCTION     W  CREATE FUNCTION public.update_relationship(rel_id integer, pub_id integer, part_id integer, new_price double precision) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE participantAndPublicatonsRelationship
    SET id_publication = pub_id, id_participant = part_id, price = new_price  
    WHERE id_relationship = rel_id;
END;
$$;
 w   DROP FUNCTION public.update_relationship(rel_id integer, pub_id integer, part_id integer, new_price double precision);
       public          postgres    false            �            1255    26513 L   update_smi(integer, character varying, character varying, character varying)    FUNCTION     +  CREATE FUNCTION public.update_smi(smi_id integer, smi_name character varying, smi_type character varying, smi_contact character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE smi SET name = smi_name, type = smi_type, contact_info = smi_contact WHERE id_smi = smi_id;
END;
$$;
 �   DROP FUNCTION public.update_smi(smi_id integer, smi_name character varying, smi_type character varying, smi_contact character varying);
       public          postgres    false            �           1255    26553    avg_price(double precision) 	   AGGREGATE     �   CREATE AGGREGATE public.avg_price(double precision) (
    SFUNC = public.price_avg_accum,
    STYPE = double precision[],
    INITCOND = '{0,0}',
    FINALFUNC = public.price_avg_final
);
 3   DROP AGGREGATE public.avg_price(double precision);
       public          postgres    false    265    264            �            1259    26483    logs    TABLE     �   CREATE TABLE public.logs (
    log_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    log_level character varying(10),
    message text
);
    DROP TABLE public.logs;
       public         heap    postgres    false                       0    0 
   TABLE logs    ACL     X   GRANT ALL ON TABLE public.logs TO admin_r;
GRANT SELECT ON TABLE public.logs TO user_r;
          public          postgres    false    223            �            1259    26443    publications    TABLE     C  CREATE TABLE public.publications (
    id_publication integer NOT NULL,
    id_smi integer NOT NULL,
    category character varying(100) NOT NULL,
    title character varying(255) NOT NULL,
    summary text NOT NULL,
    publication_date date NOT NULL,
    last_edited timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
     DROP TABLE public.publications;
       public         heap    postgres    false                       0    0    TABLE publications    ACL     h   GRANT ALL ON TABLE public.publications TO admin_r;
GRANT SELECT ON TABLE public.publications TO user_r;
          public          postgres    false    218            �            1259    26434    smi    TABLE     �   CREATE TABLE public.smi (
    id_smi integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(100) NOT NULL,
    contact_info character varying(255)
);
    DROP TABLE public.smi;
       public         heap    postgres    false                       0    0 	   TABLE smi    ACL     V   GRANT ALL ON TABLE public.smi TO admin_r;
GRANT SELECT ON TABLE public.smi TO user_r;
          public          postgres    false    216            �            1259    26500    mat_view_publication_summary    MATERIALIZED VIEW     �   CREATE MATERIALIZED VIEW public.mat_view_publication_summary AS
 SELECT s.name,
    p.category,
    count(*) AS total
   FROM (public.publications p
     JOIN public.smi s ON ((p.id_smi = s.id_smi)))
  GROUP BY s.name, p.category
  WITH NO DATA;
 <   DROP MATERIALIZED VIEW public.mat_view_publication_summary;
       public         heap    postgres    false    216    216    218    218            �            1259    26467 %   participantandpublicatonsrelationship    TABLE     �   CREATE TABLE public.participantandpublicatonsrelationship (
    id_relationship integer NOT NULL,
    id_publication integer NOT NULL,
    id_participant integer NOT NULL,
    price double precision NOT NULL
);
 9   DROP TABLE public.participantandpublicatonsrelationship;
       public         heap    postgres    false                       0    0 +   TABLE participantandpublicatonsrelationship    ACL     �   GRANT ALL ON TABLE public.participantandpublicatonsrelationship TO admin_r;
GRANT SELECT ON TABLE public.participantandpublicatonsrelationship TO user_r;
          public          postgres    false    222            �            1259    26466 9   participantandpublicatonsrelationship_id_relationship_seq    SEQUENCE     �   CREATE SEQUENCE public.participantandpublicatonsrelationship_id_relationship_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 P   DROP SEQUENCE public.participantandpublicatonsrelationship_id_relationship_seq;
       public          postgres    false    222                       0    0 9   participantandpublicatonsrelationship_id_relationship_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public.participantandpublicatonsrelationship_id_relationship_seq OWNED BY public.participantandpublicatonsrelationship.id_relationship;
          public          postgres    false    221                        0    0 B   SEQUENCE participantandpublicatonsrelationship_id_relationship_seq    ACL     �   GRANT ALL ON SEQUENCE public.participantandpublicatonsrelationship_id_relationship_seq TO admin_r;
GRANT SELECT ON SEQUENCE public.participantandpublicatonsrelationship_id_relationship_seq TO user_r;
          public          postgres    false    221            �            1259    26458    participants    TABLE     �   CREATE TABLE public.participants (
    id_participant integer NOT NULL,
    surname character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    role character varying(255) NOT NULL,
    contact_info character varying(255)
);
     DROP TABLE public.participants;
       public         heap    postgres    false            !           0    0    TABLE participants    ACL     h   GRANT ALL ON TABLE public.participants TO admin_r;
GRANT SELECT ON TABLE public.participants TO user_r;
          public          postgres    false    220            �            1259    26457    participants_id_participant_seq    SEQUENCE     �   CREATE SEQUENCE public.participants_id_participant_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.participants_id_participant_seq;
       public          postgres    false    220            "           0    0    participants_id_participant_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.participants_id_participant_seq OWNED BY public.participants.id_participant;
          public          postgres    false    219            #           0    0 (   SEQUENCE participants_id_participant_seq    ACL     �   GRANT ALL ON SEQUENCE public.participants_id_participant_seq TO admin_r;
GRANT SELECT ON SEQUENCE public.participants_id_participant_seq TO user_r;
          public          postgres    false    219            �            1259    26529    publications_history    TABLE       CREATE TABLE public.publications_history (
    id_history integer NOT NULL,
    id_publication integer NOT NULL,
    category character varying(100) NOT NULL,
    title character varying(255) NOT NULL,
    summary text NOT NULL,
    publication_date date NOT NULL,
    last_edited timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    change_type character varying(20) NOT NULL
);
 (   DROP TABLE public.publications_history;
       public         heap    postgres    false            $           0    0    TABLE publications_history    ACL     ;   GRANT ALL ON TABLE public.publications_history TO admin_r;
          public          postgres    false    227            �            1259    26528 #   publications_history_id_history_seq    SEQUENCE     �   CREATE SEQUENCE public.publications_history_id_history_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 :   DROP SEQUENCE public.publications_history_id_history_seq;
       public          postgres    false    227            %           0    0 #   publications_history_id_history_seq    SEQUENCE OWNED BY     k   ALTER SEQUENCE public.publications_history_id_history_seq OWNED BY public.publications_history.id_history;
          public          postgres    false    226            &           0    0 ,   SEQUENCE publications_history_id_history_seq    ACL     M   GRANT ALL ON SEQUENCE public.publications_history_id_history_seq TO admin_r;
          public          postgres    false    226            �            1259    26442    publications_id_publication_seq    SEQUENCE     �   CREATE SEQUENCE public.publications_id_publication_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.publications_id_publication_seq;
       public          postgres    false    218            '           0    0    publications_id_publication_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.publications_id_publication_seq OWNED BY public.publications.id_publication;
          public          postgres    false    217            (           0    0 (   SEQUENCE publications_id_publication_seq    ACL     �   GRANT ALL ON SEQUENCE public.publications_id_publication_seq TO admin_r;
GRANT SELECT ON SEQUENCE public.publications_id_publication_seq TO user_r;
          public          postgres    false    217            �            1259    26433    smi_id_smi_seq    SEQUENCE     �   CREATE SEQUENCE public.smi_id_smi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.smi_id_smi_seq;
       public          postgres    false    216            )           0    0    smi_id_smi_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.smi_id_smi_seq OWNED BY public.smi.id_smi;
          public          postgres    false    215            *           0    0    SEQUENCE smi_id_smi_seq    ACL     r   GRANT ALL ON SEQUENCE public.smi_id_smi_seq TO admin_r;
GRANT SELECT ON SEQUENCE public.smi_id_smi_seq TO user_r;
          public          postgres    false    215            �            1259    26493    view_publication_details    VIEW     �  CREATE VIEW public.view_publication_details AS
 SELECT p.id_publication,
    p.title,
    s.name AS media_name,
    par.name AS participant_name,
    rel.price
   FROM (((public.publications p
     JOIN public.smi s ON ((p.id_smi = s.id_smi)))
     JOIN public.participantandpublicatonsrelationship rel ON ((p.id_publication = rel.id_publication)))
     JOIN public.participants par ON ((rel.id_participant = par.id_participant)));
 +   DROP VIEW public.view_publication_details;
       public          postgres    false    222    222    222    220    220    218    218    218    216    216            Z           2604    26470 5   participantandpublicatonsrelationship id_relationship    DEFAULT     �   ALTER TABLE ONLY public.participantandpublicatonsrelationship ALTER COLUMN id_relationship SET DEFAULT nextval('public.participantandpublicatonsrelationship_id_relationship_seq'::regclass);
 d   ALTER TABLE public.participantandpublicatonsrelationship ALTER COLUMN id_relationship DROP DEFAULT;
       public          postgres    false    221    222    222            Y           2604    26461    participants id_participant    DEFAULT     �   ALTER TABLE ONLY public.participants ALTER COLUMN id_participant SET DEFAULT nextval('public.participants_id_participant_seq'::regclass);
 J   ALTER TABLE public.participants ALTER COLUMN id_participant DROP DEFAULT;
       public          postgres    false    219    220    220            W           2604    26446    publications id_publication    DEFAULT     �   ALTER TABLE ONLY public.publications ALTER COLUMN id_publication SET DEFAULT nextval('public.publications_id_publication_seq'::regclass);
 J   ALTER TABLE public.publications ALTER COLUMN id_publication DROP DEFAULT;
       public          postgres    false    217    218    218            \           2604    26532    publications_history id_history    DEFAULT     �   ALTER TABLE ONLY public.publications_history ALTER COLUMN id_history SET DEFAULT nextval('public.publications_history_id_history_seq'::regclass);
 N   ALTER TABLE public.publications_history ALTER COLUMN id_history DROP DEFAULT;
       public          postgres    false    227    226    227            V           2604    26437 
   smi id_smi    DEFAULT     h   ALTER TABLE ONLY public.smi ALTER COLUMN id_smi SET DEFAULT nextval('public.smi_id_smi_seq'::regclass);
 9   ALTER TABLE public.smi ALTER COLUMN id_smi DROP DEFAULT;
       public          postgres    false    215    216    216                      0    26483    logs 
   TABLE DATA           <   COPY public.logs (log_time, log_level, message) FROM stdin;
    public          postgres    false    223   �                 0    26467 %   participantandpublicatonsrelationship 
   TABLE DATA           w   COPY public.participantandpublicatonsrelationship (id_relationship, id_publication, id_participant, price) FROM stdin;
    public          postgres    false    222   \�                 0    26458    participants 
   TABLE DATA           Y   COPY public.participants (id_participant, surname, name, role, contact_info) FROM stdin;
    public          postgres    false    220   ��                 0    26443    publications 
   TABLE DATA           w   COPY public.publications (id_publication, id_smi, category, title, summary, publication_date, last_edited) FROM stdin;
    public          postgres    false    218   ��                 0    26529    publications_history 
   TABLE DATA           �   COPY public.publications_history (id_history, id_publication, category, title, summary, publication_date, last_edited, change_type) FROM stdin;
    public          postgres    false    227   ��       
          0    26434    smi 
   TABLE DATA           ?   COPY public.smi (id_smi, name, type, contact_info) FROM stdin;
    public          postgres    false    216   d�       +           0    0 9   participantandpublicatonsrelationship_id_relationship_seq    SEQUENCE SET     h   SELECT pg_catalog.setval('public.participantandpublicatonsrelationship_id_relationship_seq', 19, true);
          public          postgres    false    221            ,           0    0    participants_id_participant_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.participants_id_participant_seq', 14, true);
          public          postgres    false    219            -           0    0 #   publications_history_id_history_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.publications_history_id_history_seq', 38, true);
          public          postgres    false    226            .           0    0    publications_id_publication_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.publications_id_publication_seq', 24, true);
          public          postgres    false    217            /           0    0    smi_id_smi_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.smi_id_smi_seq', 1018, true);
          public          postgres    false    215            h           2606    26472 P   participantandpublicatonsrelationship participantandpublicatonsrelationship_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.participantandpublicatonsrelationship
    ADD CONSTRAINT participantandpublicatonsrelationship_pkey PRIMARY KEY (id_relationship);
 z   ALTER TABLE ONLY public.participantandpublicatonsrelationship DROP CONSTRAINT participantandpublicatonsrelationship_pkey;
       public            postgres    false    222            f           2606    26465    participants participants_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.participants
    ADD CONSTRAINT participants_pkey PRIMARY KEY (id_participant);
 H   ALTER TABLE ONLY public.participants DROP CONSTRAINT participants_pkey;
       public            postgres    false    220            j           2606    26537 .   publications_history publications_history_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.publications_history
    ADD CONSTRAINT publications_history_pkey PRIMARY KEY (id_history);
 X   ALTER TABLE ONLY public.publications_history DROP CONSTRAINT publications_history_pkey;
       public            postgres    false    227            c           2606    26451    publications publications_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_pkey PRIMARY KEY (id_publication);
 H   ALTER TABLE ONLY public.publications DROP CONSTRAINT publications_pkey;
       public            postgres    false    218            a           2606    26441    smi smi_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.smi
    ADD CONSTRAINT smi_pkey PRIMARY KEY (id_smi);
 6   ALTER TABLE ONLY public.smi DROP CONSTRAINT smi_pkey;
       public            postgres    false    216            ^           1259    26550    idx_smi_name    INDEX     <   CREATE INDEX idx_smi_name ON public.smi USING btree (name);
     DROP INDEX public.idx_smi_name;
       public            postgres    false    216            _           1259    26491    idx_smi_type    INDEX     ;   CREATE INDEX idx_smi_type ON public.smi USING hash (type);
     DROP INDEX public.idx_smi_type;
       public            postgres    false    216            d           1259    26492    publications_summary_gin    INDEX     u   CREATE INDEX publications_summary_gin ON public.publications USING gin (to_tsvector('russian'::regconfig, summary));
 ,   DROP INDEX public.publications_summary_gin;
       public            postgres    false    218    218            s           2620    26509 %   participants participant_after_delete    TRIGGER     �   CREATE TRIGGER participant_after_delete AFTER DELETE ON public.participants FOR EACH ROW EXECUTE FUNCTION public.participant_delete_log();
 >   DROP TRIGGER participant_after_delete ON public.participants;
       public          postgres    false    220    251            t           2620    26511 ?   participantandpublicatonsrelationship relationship_after_insert    TRIGGER     �   CREATE TRIGGER relationship_after_insert AFTER INSERT ON public.participantandpublicatonsrelationship FOR EACH ROW EXECUTE FUNCTION public.relationship_insert_log();
 X   DROP TRIGGER relationship_after_insert ON public.participantandpublicatonsrelationship;
       public          postgres    false    252    222            n           2620    26505    smi smi_after_insert    TRIGGER     r   CREATE TRIGGER smi_after_insert AFTER INSERT ON public.smi FOR EACH ROW EXECUTE FUNCTION public.smi_insert_log();
 -   DROP TRIGGER smi_after_insert ON public.smi;
       public          postgres    false    216    249            o           2620    26543 /   publications trigger_delete_publication_history    TRIGGER     �   CREATE TRIGGER trigger_delete_publication_history BEFORE DELETE ON public.publications FOR EACH ROW EXECUTE FUNCTION public.delete_publication_history();
 H   DROP TRIGGER trigger_delete_publication_history ON public.publications;
       public          postgres    false    261    218            p           2620    26539 /   publications trigger_insert_publication_history    TRIGGER     �   CREATE TRIGGER trigger_insert_publication_history AFTER INSERT ON public.publications FOR EACH ROW EXECUTE FUNCTION public.insert_publication_history();
 H   DROP TRIGGER trigger_insert_publication_history ON public.publications;
       public          postgres    false    218    259            u           2620    26549 ;   view_publication_details trigger_publication_details_delete    TRIGGER     �   CREATE TRIGGER trigger_publication_details_delete INSTEAD OF DELETE ON public.view_publication_details FOR EACH ROW EXECUTE FUNCTION public.delete_publication_details();
 T   DROP TRIGGER trigger_publication_details_delete ON public.view_publication_details;
       public          postgres    false    224    263            v           2620    26548 ;   view_publication_details trigger_publication_details_insert    TRIGGER     �   CREATE TRIGGER trigger_publication_details_insert INSTEAD OF INSERT ON public.view_publication_details FOR EACH ROW EXECUTE FUNCTION public.insert_publication_details();
 T   DROP TRIGGER trigger_publication_details_insert ON public.view_publication_details;
       public          postgres    false    224    262            w           2620    26499 ;   view_publication_details trigger_publication_details_update    TRIGGER     �   CREATE TRIGGER trigger_publication_details_update INSTEAD OF UPDATE ON public.view_publication_details FOR EACH ROW EXECUTE FUNCTION public.update_publication_details();
 T   DROP TRIGGER trigger_publication_details_update ON public.view_publication_details;
       public          postgres    false    248    224            q           2620    26507 '   publications trigger_update_last_edited    TRIGGER     �   CREATE TRIGGER trigger_update_last_edited BEFORE UPDATE ON public.publications FOR EACH ROW EXECUTE FUNCTION public.update_last_edited();
 @   DROP TRIGGER trigger_update_last_edited ON public.publications;
       public          postgres    false    218    250            r           2620    26541 /   publications trigger_update_publication_history    TRIGGER     �   CREATE TRIGGER trigger_update_publication_history BEFORE UPDATE ON public.publications FOR EACH ROW EXECUTE FUNCTION public.update_publication_history();
 H   DROP TRIGGER trigger_update_publication_history ON public.publications;
       public          postgres    false    260    218            l           2606    26478 _   participantandpublicatonsrelationship participantandpublicatonsrelationship_id_participant_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.participantandpublicatonsrelationship
    ADD CONSTRAINT participantandpublicatonsrelationship_id_participant_fkey FOREIGN KEY (id_participant) REFERENCES public.participants(id_participant) ON DELETE CASCADE;
 �   ALTER TABLE ONLY public.participantandpublicatonsrelationship DROP CONSTRAINT participantandpublicatonsrelationship_id_participant_fkey;
       public          postgres    false    4710    222    220            m           2606    26473 _   participantandpublicatonsrelationship participantandpublicatonsrelationship_id_publication_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.participantandpublicatonsrelationship
    ADD CONSTRAINT participantandpublicatonsrelationship_id_publication_fkey FOREIGN KEY (id_publication) REFERENCES public.publications(id_publication) ON DELETE CASCADE;
 �   ALTER TABLE ONLY public.participantandpublicatonsrelationship DROP CONSTRAINT participantandpublicatonsrelationship_id_publication_fkey;
       public          postgres    false    4707    218    222            k           2606    26452 %   publications publications_id_smi_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_id_smi_fkey FOREIGN KEY (id_smi) REFERENCES public.smi(id_smi) ON DELETE CASCADE;
 O   ALTER TABLE ONLY public.publications DROP CONSTRAINT publications_id_smi_fkey;
       public          postgres    false    216    218    4705                       0    26500    mat_view_publication_summary    MATERIALIZED VIEW DATA     ?   REFRESH MATERIALIZED VIEW public.mat_view_publication_summary;
          public          postgres    false    225    4886               :  x���͎���5������o�Q$6�/ {,#K lF,c��$'�"e�Ar�e�-T�QN��?f���t׼����ꙟ�J���_�ڌ�I�Fn{����k���o^Y?޿�~�~�~�~���?X���߬�S�ϯ������v��_s������S5k7�Nk+K��ck�����������z��{~���&�o�3�?=���ߛe�_�?:<|8�}1˝�q���}r���7�ؼ��F6W7׮�}�������q��=ݒ��t�Ķ[S��_n�Oֿ������s���<���������{���I��,�Nm7�mG�r\�Of�O�.6w��Ns�F����=�Ճ��s��h��F:.�t<�R�9$��L}�^l9a�)[��rΖ��l��-��4^�zp.�'c��p6����p<���!�q·��8�C�|���!p>·��P�����p>·��P8
���|���a�op>·��08���|8����p>·ӿ���p8���|8����p>�G��8A��
�G��8�#�|$����p>�G��H���p>�G��(8��|����Qp>
�G����|4�����p>�G��h8��|4̓��@��B��D��F��H��J��L��N��P��I�)�N
�鸦㜎{:긨�N���Q}Ъ>hV���-냦�A���q}к>h^���-�&�A���}��>hf���-탦�A[���}��>hn���-�&�A����}��>hv���-�A����}��>h~���-��&�A��~�
?h����-��A[��1~�?h����-�&�A���Q~�*?h����-��A���q~�:?h����-�&�A��F/��m�B��F/��m�B��F/��m�B��F/��m�B��F/��m�����Ο�N'?�?�?�?�?�?�6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h���6z��^h�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W���J=~�z�:��������ǯU�_��Z=~�z��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z��^i�W��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7����M���㷕��+O'��<~ky������i�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���h�7��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6z���i�w��6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>h���6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6���>i�O��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����h�/��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6����i�o��6���H�o�ro~��GW�e#��d��Vf�?V�x���������z��`�zs^����8��0_���zc3�N|g9{;?��Q�������ly����k�Nrۚ?�����{���o+,�����-<����qn~��*of#_̟=�6k��������-/��eÖ���ݿ�������r���Ȱzf��ͷ��7;u�j����ù�u����wn��������|c�ګ�����v����On�u����O]h�0��L�E}��-�n����lKy����Yl��O���;'7/V��ϭ�y�K�_.�_/��u��a�^G�����a���osY����8;����\g�L�_l�?��������sJ�v�X�ɹ'��ƶs�#a����!5�b�0�����+Ӈ�1Y?Nѹ����#/�����%��Q��Vqu��� ;�y�)��*ߺs�B�b�y�~���G�<:����O��f�lξ��c����;�+��m����ْnd�tft:\�1}�s���{�792�7����r=�����X?��NO�}��d3k��{���ֆG��Rٜ޺�L����a�G�;�%���yX��^���^?=��y���ɭӛ�ߺ񤞝fz�,�0�9^�0Y�{�OZ��R���\Fu鑓��黧������;[#.b�3�G[]����3�㨘��c�����>���R����94����:W�^�:귅�e�B�k��[f�4?@-%C_lN_����$���e�*�\����+W�k�OF         C   x�M���0�f����t�9����I���DŦs���
���K՘�IJ&|T�D��E�� ?�          �   x�U��N�@EׯCȞ!1M��A:�4e[*{]�1#&~@S���-�p�y�����{��w����P�A��{^�^sVK�P�R�2?6�x>�z��y�;�T��$ؠ���{z�Z��\��41�ߙ��Ԕ�?v�#�X�<���gY8S�Pk�0�<�1ɟ#�QG�N�h�	_����Ҝ/���\�hjn��q���.ϗ8��~��-�#�ԕ���:0q�i��<���o��         �  x��S�j�@<��b��b߮���-����Ǹ%�JJ��4����XX�c���Q�l�u
	��3���[�"ŏ�����[��B��p��W�V�c����[�j�SV�����y�;����}$���.܅/��ּ<
��<���N�5֍Ɏ�2�llM�"��Mr�J�?7JU��7w������=T[QsT����Q���+�6�	���'�t����8pm�;�7� $_�P�k�i S��_к��ۨ�r��A�AVMt�v_f�#)�1ly]�:�AG���?�8��qh�U�Q�y	�F:�#y��ѯ�x:�X��(�!#�n#E֍��1�
&ї��a���5EiI�x9��Z��d:��:6f �9GZ��l�XkR�r$�������嬞�z6�
a�?���r0+*�ܗYٓ3E��?��!�F+����5#M��U�Ԧ�RWY�d���cܩ�j*v䪣�,2��$#�r��\R�ܙ8��d4�Ȫَ         �  x���ˎE����}�ҩS��E�,�Bv�b˳cc���L@)�l�p�����x^������v���h���]}9_��Rǥ��k����"]���E�JoӲ}%�/�nn����"ͫ���L׸�Is�~N�h�^T�~��w�ίӪ»k<|�뼽l���0\���)���R0�**�C3$;�P)_+UK�:z������'�������{���>�D/#9C�O-�O�~>�#&��B��:�Yl���v�7�y�M�}�߼κ�������e�<<Z�
��=}r����fz�~U�[H�Zf�o�оC�b���k�%��Ve�G�|~��Ӂ}X�F�^�ߐ.$���s���[����&S[#�sQ�B�A@�-]�[�������x�2Fc�/`�A`�*�G`��n�ᚂd��S�{��M{Yp����B	��f�׮ī{�Q�]96��28�)������E��7�N,�y^�b��5�_�a]+-�&�zR�Ah�6[к���b���uq��
�D.��^9��@S_t' 7��sy�3�$�r&�N�SA���m���C�ڼl�d,���(P��I>��F�����!h�9��!�Uf����7����)L�bڛ�<��&���N#��d��]��|<5��h���0�bU�P+#�w�p�1�a�X�b��G�����&�-�14�(�ɨ?Q�Z��$��I�<�jr>)��wbU bFF��2��4L���Fݦ�?j��6�<kFpa�L�5<���6��V�ʦ�����y�\�(j��j�!�fhf#X��#��S@ZJ�U��G����H�5V�Ŗ��`�K\�7w���
�6���Ķ/2���v:D�(����*���4�c!�v�:CR[CE�^u�%�pS����u�|�0�d��`�Ό�����A ��|4]l%�#hT�����r��� H�}�      
   �   x���=
�@���S�#J��F$J@HVm���6"�?'X�A��3���EPD,f�ݙ7�۱3#�UO�qC���?e�9�H����[�#��[��Ad�=Q!l�#�d�ܝs\{�_8�p��sN���є�%���J�>hC�f|��
��oa��ڄSv�P���n���5��1�g�ڲʖM�] 5�����cgg��p�2u�Ǣn
!�j���     