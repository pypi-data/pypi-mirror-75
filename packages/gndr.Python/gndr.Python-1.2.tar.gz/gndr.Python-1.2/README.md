# gndr (Python Edition): Determine gender programmatically

[Orginal Package](https://github.com/tjhorner/gndr)

`gndr` is a breakthrough in automated gender detection.

It uses advanced techniques and algorithms to determine the gender of a user by **just fucking asking them.**

The API couldn't be simpler. All you need to do is **ask the user what gender they identify as** along with **what pronouns they use**, and the library will give you back which gender they are with 100% accuracy. Incredible.

## Example
```Python
from gndr import identifyGender

gender = identifyGender(gender="Non-binary", pronouns=["They", "Them"])
gender.get() # Returns gender and pronouns
```

## License

MIT, but I hope you aren't actually thinking of using this

Example

License
MIT, but I hope you aren't actually thinking of using this