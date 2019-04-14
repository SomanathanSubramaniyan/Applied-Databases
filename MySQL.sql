
-- SECTION 4.1
-- 4.1 MySQL Import the world database from world.sql to MySQL
--------------------------------------------
-- C:\Program Files\MySQL\MySQL Server 8.0\bin>mysql -uroot -pXXX <"C:\Users\soman\Documents\Hdip Data Analytics - 2019\Applied-Databases\Project\world.sql"
-- mysql: [Warning] Using a password on the command line interface can be insecure.
-- New database created in MySQL
--------------------------------------------
-- SECTION 4.1.1
-- Get people who have visited a particular country Write a MySQL procedure called get_ppl_visited_country that takes one parameter of type varchar(52) 
-- which represents the name particular country. 
-- The procedure should display the following details of people who have visited that country: • The person’s ID • The person’s name • The name of the city/cities the person -- visited in the country • The date the person arrived in the city/cities • The country’s full name 
-------------------------------------------------------------------------
-- Answer to 4.1.1 STARTS HERE ------------------------------------------
-------------------------------------------------------------------------
Drop procedure get_ppl_visited_country;
DELIMITER //
CREATE PROCEDURE get_ppl_visited_country (IN cty varchar(52))
BEGIN
  SET @cty = CONCAT("%", cty, "%");
  select 	
		a.personID, 
        a.personname, 
		c.name, 
        b.dateArrived,
	    (select d.name from country d where d.code = c.countrycode) CountryName
        from (( person a
Inner join	hasvisitedcity b ON  a.personID = b.personID)
Inner join	city c ON b.cityId = c.id)
where c.countrycode in (select e.code from country e where e.name like @cty);
END //
DELIMITER ;
call get_ppl_visited_country("a");
----------------------------------------------------------------------
-- Answer to 4.1.1 ENDS HERE ------------------------------------------
-----------------------------------------------------------------------
-- 4.1.2 Rename Continent Write a function that called ren_continent 
-- that takes one parameter which is a Continent name and returns the New Name associated with the Continent name 
-----------------------------------------------------------------------
-- Answer to 4.1.2 STARTS HERE ------------------------------------------
-------------------------------------------------------------------------
Drop function ren_continent;
DELIMITER //
Create function ren_continent (ocontinent VARCHAR(90)) RETURNS VARCHAR(50) DETERMINISTIC
Begin
DECLARE ncontinent varchar(50);
    IF(ocontinent like 'North America' or ocontinent like 'South America') Then
		SET ncontinent = "Americas";
	ELSEIF ocontinent = "Oceania" Then
		SET ncontinent = "Australia";
	elseif ocontinent = "Antartica" Then
		SET ncontinent = "South Pole";
	END IF;
Return (ncontinent);
end //
DELIMITER ;
Select ren_continent("Antartica");
-----------------------------------------------------------------------
-- Answer to 4.1.2 ENDS HERE ------------------------------------------
------------------------------------------------------------------------
-- 4.1.3 Country with biggest population per continent Give the MySQL command to show the continent, 
-- and the name and population of the country with the biggest population in each continent. 
-- NOTE: Only include countries where the population is greater than 0. 
-----------------------------------------------------------------------
-- Answer to 4.1.3 STARTS HERE ----------------------------------------
------------------------------------------------------------------------

Select a.continent, a.name, a.population
from country a
where a.population >0
and a.population = (select max(b.population) from country b where b.continent = a.continent)
order by a.continent,a.name,a.population;
-----------------------------------------------------------------------
-- Answer to 4.1.3 ENDS HERE ------------------------------------------
------------------------------------------------------------------------
-- 4.1.4 Minimum city population of youngest person(s) Give the MySQL command to show the name/names 
-- of the city/cities with the lowest population, that the youngest person/persons has/have visited. 
-----------------------------------------------------------------------
-- Answer to 4.1.4 STARTS HERE ----------------------------------------
------------------------------------------------------------------------
select 
c.name City,f.name Country,f.population population from   
(( country f
Inner join	city c ON c.countrycode = f.code)
Inner join	hasvisitedcity d ON  d.cityId = c.id )
where 
d.personID in (select a.personID from person a where a.age = (select min(b.age) from person b))
and f.population = (select min(g.population) from country g
					where g.code in (select cy.countrycode from city cy where 
										cy.id in (select hy.cityid from hasvisitedcity hy where
													hy.personID in (select pn.personID from person pn 
																	where pn.age = (select min(pn2.age) from person pn2)))));
-----------------------------------------------------------------------
-- Answer to 4.1.4 ENDS HERE ------------------------------------------
------------------------------------------------------------------------
-- 4.1.5 Update City Populations Write a single MySQL command to increase the population of South African cities depending on their district as follows: 
-----------------------------------------------------------------------
-- Answer to 4.1.5 STARTS HERE ----------------------------------------
------------------------------------------------------------------------
select district,
case
	when district = "Western Cape"
	then sum(population)-10000  
	when district = "Free State"
	then sum(population)+2000
	when district = "Eastern Cape"
	then sum(population)+1000
    else sum(population) 
end  population   
from city  
where countrycode in (select code from country where name like "%south%africa%")
group by district;
----------------------------------------------------------------------
---- Answer to 4.1.5 ENDS HERE ----------------------------------------
------------------------------------------------------------------------
-- 4.1.6 Country Independence Write a MySQL query show the name and year of independence of each country, 
-- as well as a column called “Desc” which has the following information. 
----------------------------------------------------------------------
---- Answer to 4.1.6 STARTS HERE -------------------------------------
----------------------------------------------------------------------
select name, Indepyear, 
case
	when Indepyear is null 
    then "N/A" 
    when cast(year(curdate()) as signed) - Indepyear < 10 
    then Concat("New ",GovernmentForm)
    when (cast(year(curdate()) as signed) - Indepyear >= 10)  AND (cast(year(curdate()) as signed) - Indepyear < 50)
    then Concat("Modern ",GovernmentForm)
    when (cast(year(curdate()) as signed) - Indepyear >= 50)  AND (cast(year(curdate()) as signed) - Indepyear < 100)
    then Concat("Early ",GovernmentForm)
	when (cast(year(curdate()) as signed) - Indepyear >= 100)
    then Concat("Old ",GovernmentForm)
    else "old"    
end Description
from country
order by Indepyear;
----------------------------------------------------------------------
---- Answer to 4.1.6 ENDs HERE ---------------------------------------
----------------------------------------------------------------------



