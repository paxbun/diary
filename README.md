# Diary

My diary format spec

# Examples

```
# 2021-12-23

* 0800-1200 with Chanjung, Foo at E16
  * Had discussion about C++20 modules
  * Has discussion about C++20 ranges
* 1700-1800: Read a NLP paper
  * Made a server with ASP.NET Core
* 2100-0100: Other stuffs

# 2021-12-24

* 0800-1200 with Chanjung, Foo at E16
  * Had discussion about C++20 modules
  * Has discussion about C++20 ranges
* 1300-1500
  * Made a server with ASP.NET Core
* 1700-1800: Read a NLP paper
* 2100-0100: Other stuffs

# TODO: December 26th, 2021

* 1300-1500
  * Make a server with ASP.NET Core
* 1700-1800: Read a NLP paper
```

# Example Result (`python main.py`)
```
2021-12-23 (worked 9:00:00)
* Had discussion about C++20 modules
* Has discussion about C++20 ranges 
* Read a NLP paper
* Made a server with ASP.NET Core   
* Other stuffs

2021-12-24 (worked 11:00:00)        
* Had discussion about C++20 modules
* Has discussion about C++20 ranges 
* Made a server with ASP.NET Core   
* Read a NLP paper
* Other stuffs

Total time worked: 20:00:00
```